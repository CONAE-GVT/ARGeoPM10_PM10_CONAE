import datetime as dt
import glob
import itertools
import json
import math
import os

from collections import defaultdict
from pyspatialml import Raster
from typing import Any, DefaultDict, Dict, List, Tuple


from empatia.etl.merra_data_source import get_merra_files
from empatia.etl.modis_data_source import get_modis_files
from empatia.etl.transformers import get_modis_mosaic, get_viirs_mosaic
from empatia.model.estimator import PM10Estimator
from empatia.settings import (
    DAILY_PM10_TEMPLATE_PATH,
    DOMAIN_DATA_PATH,
    ICA_COLOR_RULES_PATH,
    ICA_TEMPLATE_PATH,
    MERRA_DATASET_PATH,
    MODEL_PATH,
    MODIS_DATASET_PATH,
    MONTHLY_PRODUCT_TEMPLATES,
    PM10_COLOR_RULES_PATH,
    PREDICTION_DATA_PATH,
    PROCESSED_DATA_PATH,
    REGION_DATA_PATH,
)
from empatia.settings.constants import (
    DAILY_PM10_METADATA_CODES,
    DEFAULT_DATE_FORMAT,
    ICA_PATH,
    ICA_PM10_METADATA_CODES,
    MAIAC_BANDS,
    MAIAC_COLLECTION,
    MAIAC_PRODUCT,
    MERRA_DATASETS,
    MERRA_SHORTNAME,
    MIN_PERCENTAGE_OF_VALID_DATA,
    MODIS_REGION,
    MONTHLY_PM10_METADATA_CODES,
    MONTHLY_PRODUCT_CODES,
    NODATA,
    PM10_PREFIX_FILENAME,
    SENSORS,
    VIIRS_COLLECTION,
    VIIRS_DATE_END,
    VIIRS_DATE_START,
    VIIRS_PRODUCT,
    XML_MERRA_PRODUCT_NAMES,
    XML_VIIRS_NAME,
)
from empatia.settings.log import logger
from empatia.utils import (
    create_xml,
    date_range,
    get_qa_class,
    remove_file,
    remove_folders_from_date,
    zip_directory,
)
from empatia.utils.grass import (
    apply_mask,
    clean_db,
    compute_mean,
    compute_stddev,
    discretize_values,
    enough_valid_data_has_been_collected,
    export_multiband_gtiff,
    get_count,
    get_number_of_null_values,
    get_ranges,
    get_resampling,
    import_gtiff,
    import_netcdf,
    raster2gtiff,
    raster2png,
    refresh_region,
    remove_mask,
    reset_color_table,
    set_domain,
)


def viirs_etl() -> None:
    """
    Compute the mean of April, May and June of the product `VNP46A1`.
    """

    today = dt.datetime.today()
    date_start = dt.datetime.strptime(VIIRS_DATE_START, DEFAULT_DATE_FORMAT)
    date_end = dt.datetime.strptime(VIIRS_DATE_END, DEFAULT_DATE_FORMAT)
    output_dir = f"{PROCESSED_DATA_PATH}/{VIIRS_PRODUCT}_{date_start.year}/"
    ds_to_download = date_range(date_start, date_end)
    uncompleted_dates = []
    log_file = f"{output_dir}log.txt"

    if today <= date_end:
        logger.info("Unable to update VIIRS data yet")
        return None

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    if os.path.exists(log_file):
        with open(log_file) as json_file:
            log_data = json.load(json_file)
            status = log_data["status"]
            ds_to_download = log_data["uncompleted_dates"]
        if status == "OK":
            logger.info("VIIRS data already updated")
            return None

    logger.info("Running VIIRS ETL")

    logger.info("Setting domain...")
    set_domain(DOMAIN_DATA_PATH)
    apply_mask(REGION_DATA_PATH)

    logger.info("Downloading VIIRS data...")
    viirs_rasters = []
    for ds in ds_to_download:
        try:
            logger.info(f"Date: {ds}")
            if not get_modis_files(
                VIIRS_PRODUCT,
                VIIRS_COLLECTION,
                start_date=ds,
                **MODIS_REGION,  # type: ignore
            ):
                continue

            outname = f"viirs_{ds}"
            current_viirs_path = f"{MODIS_DATASET_PATH}/{VIIRS_PRODUCT}/{ds}/"
            get_viirs_mosaic(current_viirs_path, 4, output_dir, f"{outname}.tif")
            import_gtiff(f"{output_dir}{outname}.tif", outname)
            viirs_rasters.append(outname)
        except Exception as e:
            logger.error(f"Not found VIIRS for {ds}: {e}")
            uncompleted_dates.append(ds)

    logger.info("Computing VIIRS average...")
    try:
        raster_name = f"viirs_night_lights_{date_start.year}"
        compute_mean(viirs_rasters, raster_name)
        refresh_region()
        raster2gtiff(raster_name, f"{output_dir}{raster_name}")
        log_data = {"status": "OK", "uncompleted_dates": uncompleted_dates}
    except Exception as e:
        logger.error(f"Uncompleted VIIRS update: {e}")
        log_data = {"status": "FAIL", "uncompleted_dates": uncompleted_dates}

    with open(log_file, "w") as outfile:
        json.dump(log_data, outfile)

    return None


def get_viirs_dataset_path(year: int) -> str:
    """
    Get the available path of the VIIRS feature
    """
    viirs_path = (
        f"{PROCESSED_DATA_PATH}/{VIIRS_PRODUCT}_{year}/viirs_night_lights_{year}.tif"
    )

    return viirs_path


def clean_storages(ndays: int) -> None:
    """
    Clean obsolete data, files and folders from `current date - ndays`
    """

    logger.info("Cleaning GRASS data base...")
    clean_db()
    logger.info("Cleaning directories...")
    today = dt.datetime.today()
    start_date = today - dt.timedelta(days=ndays)
    # Remove MAIAC datasets
    pattern = f"{MODIS_DATASET_PATH}/{MAIAC_PRODUCT}/*"
    remove_folders_from_date(pattern, start_date)
    # Remove MERRA datasets
    for dataset in MERRA_DATASETS:
        shortname = dataset.get("shortname", "")
        pattern = f"{MERRA_DATASET_PATH}/{shortname}/*"
        remove_folders_from_date(pattern, start_date)
    # Remove processing folder
    pattern = f"{PROCESSED_DATA_PATH}/*"
    remove_folders_from_date(pattern, start_date)
    # Remove prediction folder
    pattern = f"{PREDICTION_DATA_PATH}/*"
    remove_folders_from_date(pattern, start_date)


def predict(model: Any, rfiles: List, outname: str) -> None:
    """
    Get prediction for a given date
    Args:
        model: model object to estimate PM10
        rfile: TIFF files, model feature
        outname: name of the output raster map
    """
    stack = Raster(rfiles)
    prediction = stack.predict(estimator=model)

    _ = prediction.write(file_path=f"{outname}.tif", nodata=NODATA)


def daily_pipeline(start_date: str = None, end_date: str = None) -> None:
    """
    Compute the following daily products:
        PM10 per sensor orbit
        ICA
    """
    estimator = PM10Estimator.load_model(MODEL_PATH)
    log_file = f"{PROCESSED_DATA_PATH}/log.txt"
    today = dt.datetime.today()

    dates_to_download = (
        get_dates_to_download_for_a_range(start_date, end_date)
        if start_date
        else get_dates_to_download(log_file, today)
    )

    logger.info("Get VIIRS data")
    viirs_file_path = get_viirs_dataset_path(today.year)
    if not os.path.exists(viirs_file_path):
        viirs_file_path = get_viirs_dataset_path(today.year - 1)

    logger.info("Setting domain...")
    set_domain(DOMAIN_DATA_PATH)
    apply_mask_result = apply_mask(REGION_DATA_PATH)
    total_cells = get_total_cells(apply_mask_result)

    logger.info("Processing...")
    new_uncompleted_dates = []
    for date in dates_to_download:
        logger.info(f"Date: {date}")
        processed_dir_path = f"{PROCESSED_DATA_PATH}/{date}/"
        try:
            if not os.path.exists(processed_dir_path):
                os.mkdir(processed_dir_path)

            prediction_dir_path = f"{PREDICTION_DATA_PATH}/{date}/"
            if not os.path.exists(prediction_dir_path):
                os.mkdir(prediction_dir_path)

            logger.info("Downloading MAIAC data...")
            current_maiac_path = f"{MODIS_DATASET_PATH}/{MAIAC_PRODUCT}/{date}/"
            modis_outputs = process_modis_data(
                current_maiac_path, date, processed_dir_path, total_cells
            )
            if not modis_outputs:
                continue

            logger.info("Downloading MERRA data...")
            process_merra_data(date, modis_outputs, processed_dir_path)

            logger.info("Computing PM10...")
            creation_date, log_prediction, min_date = computing_pm_10(
                current_maiac_path,
                modis_outputs,
                estimator,
                prediction_dir_path,
                processed_dir_path,
                viirs_file_path,
            )

            logger.info("Computing ICA...")
            computing_ica(
                creation_date,
                log_prediction,
                min_date,
                prediction_dir_path,
                processed_dir_path,
            )

        except Exception as e:
            logger.error(f"Uncompleted process: {e}")
            new_uncompleted_dates.append(date)

        delete_intermediate_files(processed_dir_path)

    update_log_data(dates_to_download, log_file, new_uncompleted_dates)


def update_log_data(
    dates_to_download: List[str], log_file: str, new_uncompleted_dates: List[str]
) -> None:
    last_execution_date = dates_to_download[-1]
    log_data = {
        "last_execution_date": last_execution_date,
        "uncompleted_dates": sorted(set(new_uncompleted_dates)),
    }
    with open(log_file, "w") as outfile:
        json.dump(log_data, outfile)


def delete_intermediate_files(processed_dir_path: str) -> None:
    files_to_del = glob.glob(f"{processed_dir_path}*.tif")
    files_to_preserve = glob.glob(f"{processed_dir_path}CONAE*")
    files_to_del = set(files_to_del) - set(files_to_preserve)  # type: ignore
    for ftd in files_to_del:
        os.remove(ftd)


def computing_ica(
    creation_date: str,
    log_prediction: DefaultDict[Any, List],
    min_date: dt.date,
    prediction_dir_path: str,
    processed_dir_path: str,
) -> None:
    pattern = f"{processed_dir_path}{PM10_PREFIX_FILENAME}_*.tif"
    daily_predictions = sorted(glob.glob(pattern))
    products = []
    ica_rasters = []
    for e, dp in enumerate(daily_predictions):
        rname = f"daily_prediction_{e}"
        ica_rasters.append(rname)
        # Import to GRASS
        import_gtiff(dp, rname)
        products.append(dp.split("/")[-1].split(".")[0])
    refresh_region()
    ica_file = f"{ICA_PATH}_{min_date.strftime('%Y%m%d')}_v001"
    ica_dir = f"{prediction_dir_path}{ica_file}/"
    if not os.path.exists(ica_dir):
        os.mkdir(ica_dir)
    # Compute daily mean
    compute_mean(ica_rasters, "daily_ica")
    # Reclassified prediction
    rname = "ICA"
    discretize_values("daily_ica", get_qa_class, rname)
    _max, _min = get_ranges(rname)
    # Export Gtiff
    reset_color_table(rname, ICA_COLOR_RULES_PATH)
    export_multiband_gtiff([rname], ica_file, f"{ica_dir}{ica_file}", NODATA)
    # raster2gtiff(rname, f"{p_dir}{ica_file}")
    # Create XML
    metadata = dict(
        zip(
            ICA_PM10_METADATA_CODES.values(),
            [
                ica_file,
                creation_date,
                _max,
                _min,
                _max,
                _min,
                ", ".join(products),
            ],
        )
    )
    # Uncomment to use metadata
    # create_xml(ICA_TEMPLATE_PATH, metadata, f"{ica_dir}{ica_file}")
    # Export PNG
    raster2png(rname, f"{ica_dir}{ica_file}")
    # Remove aux.xml temporary files
    remove_file(f"{ica_dir}/{ica_file}.aux.xml")
    # Zip directory with all product
    zip_directory(ica_dir, ica_dir)
    with open(f"{prediction_dir_path}/log.txt", "w") as outfile:
        json.dump(log_prediction, outfile, indent=4)


def computing_pm_10(
    current_maiac_path: str,
    modis_outputs: List[Any],
    estimator: str,
    prediction_dir_path: str,
    processed_dir_path: str,
    viirs_file_path: str,
) -> Tuple[str, DefaultDict[Any, List], dt.datetime]:
    log_prediction = defaultdict(list)  # type: ignore
    creation_date = dt.datetime.today().strftime("%Y-%m-%dT%H:%M:%S")
    for modis_orbit in modis_outputs:
        aod_file, sensor, min_date = modis_orbit.values()
        pattern = f"{processed_dir_path}*_{min_date.hour}_{sensor}.tif"
        features_files = sorted(glob.glob(pattern))
        features_files.pop(1)  # remove AOD_QA
        features_files.insert(4, str(DOMAIN_DATA_PATH))
        features_files.append(str(viirs_file_path))
        # Predict PM10
        pm10_file_path = (
            f"{PM10_PREFIX_FILENAME}_{min_date.strftime('%Y%m%d_%H%M%S')}_v001"
        )
        predict(estimator, features_files, f"{processed_dir_path}{pm10_file_path}")
        pm10_file = f"{processed_dir_path}{pm10_file_path}.tif"
        log_prediction[sensor].append(pm10_file)
        # Get prediction file
        pm10_band_name = "PM10"
        import_gtiff(pm10_file, pm10_band_name)
        _max, _min = get_ranges(pm10_band_name)
        reset_color_table(pm10_band_name, PM10_COLOR_RULES_PATH)
        # Get AOD associated
        aod_band_name = "QA_AOD"
        import_gtiff(aod_file, aod_band_name)
        _max2, _min2 = get_ranges(aod_band_name)
        # Export Gtiff
        pm10_dir = f"{prediction_dir_path}{pm10_file_path}/"
        if not os.path.exists(pm10_dir):
            os.mkdir(pm10_dir)

        refresh_region()
        export_multiband_gtiff(
            [pm10_band_name, aod_band_name],
            pm10_file_path,
            f"{pm10_dir}{pm10_file_path}",
            NODATA,
        )
        # Create XML
        maiac_files = [
            os.path.basename(x) for x in glob.glob(f"{current_maiac_path}*.hdf")
        ]
        merra_files = [
            fname.format(min_date.strftime("%Y%m%d"))
            for fname in XML_MERRA_PRODUCT_NAMES
        ]
        metadata = dict(
            zip(
                DAILY_PM10_METADATA_CODES.values(),
                [
                    pm10_file_path,
                    creation_date,
                    _max,
                    _min,
                    _max2,
                    _min2,
                    ", ".join(maiac_files),
                    ", ".join(merra_files),
                    XML_VIIRS_NAME.format(min_date.year),
                ],
            )
        )
        # Uncomment to use metadata
        # create_xml(DAILY_PM10_TEMPLATE_PATH, metadata, f"{pm10_dir}{pm10_file_path}")
        # Export PNG
        raster2png(pm10_band_name, f"{pm10_dir}{pm10_file_path}")
        # Remove aux.xml temporary files
        remove_file(f"{pm10_dir}/{pm10_file_path}.aux.xml")
        # Zip directory with all product
        zip_directory(pm10_dir, pm10_dir)
    return creation_date, log_prediction, min_date


def process_merra_data(date: str, modis_outputs: List[Any], processed_dir: str) -> None:
    for dataset in MERRA_DATASETS:
        shortname = dataset.get("shortname", "")
        product = dataset.get("product", "")
        variables = dataset.get("variables", [])
        get_merra_files(date, **dataset)  # type: ignore
        # Import to GRASS to reproject and rescale
        for modis_orbit, var in itertools.product(modis_outputs, variables):
            _, sensor, min_date = modis_orbit.values()
            current_merra_path = (
                f"NETCDF:{MERRA_DATASET_PATH}/{shortname}/" f"{date}/{product}.nc:{var}"
            )
            merra_band = (int(min_date.hour) % 12) + 1
            if shortname == MERRA_SHORTNAME:
                merra_band = (math.trunc(int(min_date.hour) / 3) + 1) - 4

            rname = f"{var}_{min_date.hour}_{sensor}"
            rofile = f"{processed_dir}{rname}"
            remove_mask()
            try:
                import_netcdf(current_merra_path, merra_band, rname)
            except Exception:
                os.remove(f"{MERRA_DATASET_PATH}/{shortname}/{date}/{product}.nc")
                get_merra_files(date, **dataset)  # type: ignore
                import_netcdf(current_merra_path, merra_band, rname)

            get_resampling(rname)
            apply_mask(REGION_DATA_PATH)
            refresh_region()
            raster2gtiff(rname, rofile)
    return None


def process_modis_data(
    current_maiac_path: str, date: str, processed_dir_path: str, total_cells: int
) -> List[Any]:
    if not get_modis_files(
        MAIAC_PRODUCT,
        MAIAC_COLLECTION,
        start_date=date,
        **MODIS_REGION,  # type: ignore
    ):
        return []
    null_files = []  # type: ignore
    modis_outputs = []  # type: ignore
    for band, prefix in MAIAC_BANDS.items():
        modis_outputs = get_modis_mosaic(
            current_maiac_path, band, prefix, processed_dir_path
        )
        # Import to GRASS to reproject and rescale
        orbits_to_clean = []
        for modis_orbit in modis_outputs:
            rfile, sensor, min_date = modis_orbit.values()
            sufix = f"{min_date.hour}_{sensor}"
            logger.info(f"Current sufix: {sufix}")
            rname = f"{prefix}_{sufix}"
            import_gtiff(rfile, rname)
            refresh_region()

            error_message_in_mosaic = (
                f"The current file {rname} won't be processed because the "
                f"{MIN_PERCENTAGE_OF_VALID_DATA}% floor of non-null cells was not reached"
            )
            if sufix in null_files:
                logger.info(error_message_in_mosaic)
                orbits_to_clean.append(modis_orbit)
                continue

            null_values = get_number_of_null_values(rname)
            if not enough_valid_data_has_been_collected(total_cells, null_values):
                null_files.append(sufix)
                logger.info(error_message_in_mosaic)
                orbits_to_clean.append(modis_orbit)
                continue

            logger.info(f"The current file {rname} will be processed")
            rofile = f"{processed_dir_path}{rname}"
            raster2gtiff(rname, rofile)

        for modis_orbit in orbits_to_clean:
            modis_outputs.remove(modis_orbit)
    return modis_outputs


def get_dates_to_download_for_a_range(
    start_date: str, end_date: str = None
) -> List[str]:
    if not end_date:
        return [start_date]
    date_format = "%Y-%m-%d"
    start_date_dt = dt.datetime.strptime(start_date, date_format)
    end_date_dt = dt.datetime.strptime(end_date, date_format)
    return [
        (start_date_dt + dt.timedelta(days=days)).strftime(date_format)
        for days in range((end_date_dt - start_date_dt).days + 1)
    ]


def get_dates_to_download(log_file: str, today: dt.datetime) -> List[str]:
    min_exec_date = dt.datetime.strftime(
        today - dt.timedelta(days=90), DEFAULT_DATE_FORMAT
    )
    logger.info("Running ETL ...")
    if os.path.exists(log_file):
        with open(log_file) as json_file:
            log_data = json.load(json_file)
            uncompleted_dates = log_data["uncompleted_dates"]
            date_start = dt.datetime.strptime(
                log_data["last_execution_date"], DEFAULT_DATE_FORMAT
            )
    else:
        uncompleted_dates = []
        date_start = today
    dates_to_download = list(set(uncompleted_dates + date_range(date_start, today)))
    dates_to_download = sorted(filter(lambda x: x >= min_exec_date, dates_to_download))
    return dates_to_download


def get_total_cells(result: Dict) -> int:
    cells_data = [k for k in result if k.startswith("cells")][0]
    total_cells = int(cells_data.replace(" ", "")[6:])
    logger.info(f"Total cells in Argentina: {total_cells}")
    return total_cells


def monthly_pipeline(ndays: int) -> None:
    """
    Compute the following monthly statistics:
        Mean
        Standar Desviation
        N
    """
    logger.info("Setting domain...")
    set_domain(DOMAIN_DATA_PATH)
    apply_mask(REGION_DATA_PATH)

    logger.info("Processing...")
    today = dt.datetime.today()
    start_date = today - dt.timedelta(days=ndays)
    year, month, _ = start_date.strftime(DEFAULT_DATE_FORMAT).split("-")

    # Create destination folder if it not exist
    folder = f"{PREDICTION_DATA_PATH}/monthly/"
    if not os.path.exists(folder):
        os.mkdir(folder)

    logger.info("Collecting data...")
    pattern = f"{PREDICTION_DATA_PATH}/{year}-{month}-*/log.txt"
    logs = sorted(glob.glob(pattern))
    daily_preds = defaultdict(list)  # type: ignore
    for log_file in logs:
        with open(log_file) as json_file:
            log_data = json.load(json_file)
            for key in log_data.keys():
                if key in SENSORS:
                    daily_preds[key].extend(log_data[key])

    if len(daily_preds) == 0:
        logger.info(f"Data not found for {year}-{month}")
        return None

    for sensor in SENSORS:
        logger.info(f"Getting monthly product for {sensor}")
        products = []
        rasters = []
        product_prefix = f"{sensor.lower()}_{year}_{month}"
        for e, rfile in enumerate(daily_preds[sensor]):
            rasters.append(f"{product_prefix}_{e}")
            import_gtiff(rfile, f"{product_prefix}_{e}")
            products.append(rfile.split("/")[-1].split(".")[0])

        refresh_region()
        # PM10 monthly mean
        rname = f"PM10_media_{sensor}"
        compute_mean(rasters, rname)
        _max, _min = get_ranges(rname)
        group = [rname]

        # PM10 monthly standard deviation
        rname = f"PM10_desvest_{sensor}"
        compute_stddev(rasters, rname)
        _max2, _min2 = get_ranges(rname)
        group.append(rname)

        # Amount of values
        rname = "PM10_n"
        get_count(rasters, rname)
        _max3, _min3 = get_ranges(rname)
        group.append(rname)

        # Define file name and metadata
        refresh_region()
        pcode = MONTHLY_PRODUCT_CODES[sensor]
        xml_template = MONTHLY_PRODUCT_TEMPLATES[sensor]
        creation_date = dt.datetime.today().strftime("%Y-%m-%dT%H:%M:%S")
        first_day = "".join(daily_preds[sensor][0].split("/")[-2].split("-"))
        last_day = "".join(daily_preds[sensor][-1].split("/")[-2].split("-"))
        group_name = f"{PM10_PREFIX_FILENAME}m_{first_day}_{last_day}_{pcode}_v001"
        metadata = dict(
            zip(
                MONTHLY_PM10_METADATA_CODES.values(),
                [
                    group_name,
                    creation_date,
                    _max,
                    _min,
                    _max2,
                    _min2,
                    _max3,
                    _min3,
                    ", ".join(products),
                ],
            )
        )
        # Create folder to save data
        output_dir = f"{folder}{group_name}"
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        # Export Gtiff
        export_multiband_gtiff(group, group_name, f"{output_dir}/{group_name}", NODATA)

        # Export XML
        # Uncomment to use metadata
        # create_xml(xml_template, metadata, f"{output_dir}/{group_name}")

        # Export PNG only PM10 monthly mean
        rname = f"PM10_media_{sensor}"
        reset_color_table(rname, PM10_COLOR_RULES_PATH)
        raster2png(rname, f"{output_dir}/{group_name}")

        # Remove aux.xml temporary files
        remove_file(f"{output_dir}/{group_name}.aux.xml")

        # Zip directory with all product
        zip_directory(output_dir, output_dir)
