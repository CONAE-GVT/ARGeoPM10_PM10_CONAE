from empatia.etl.checker import retrieve_dates
from empatia.etl.merra_data_source import get_merra_files
from empatia.etl.modis_data_source import get_modis_files
from empatia.settings import MERRA_DATASET_PATH, MODIS_DATASET_PATH
from empatia.settings.constants import (
    MAIAC_COLLECTION,
    MAIAC_PRODUCT,
    MERRA_DATASETS,
    MODIS_REGION,
    VIIRS_COLLECTION,
    VIIRS_PRODUCT,
)


def merra_etl() -> None:
    file_format = "nc"
    for dataset in MERRA_DATASETS:
        product = dataset.get("shortname", "")
        ds_to_download = retrieve_dates(
            MERRA_DATASET_PATH, product, file_format  # type: ignore
        )
        for ds in ds_to_download:
            get_merra_files(ds, **dataset)  # type: ignore


def maiac_etl() -> None:
    file_format = "h5"
    ds_to_download = retrieve_dates(MODIS_DATASET_PATH, MAIAC_PRODUCT, file_format)
    for ds in ds_to_download:
        get_modis_files(
            MAIAC_PRODUCT,
            MAIAC_COLLECTION,
            start_date=ds,
            file_format=file_format,
            **MODIS_REGION  # type: ignore
        )


def viirs_etl() -> None:
    file_format = "h5"
    ds_to_download = retrieve_dates(MODIS_DATASET_PATH, VIIRS_PRODUCT, file_format)
    for ds in ds_to_download:
        get_modis_files(
            VIIRS_PRODUCT,
            VIIRS_COLLECTION,
            start_date=ds,
            file_format=file_format,
            **MODIS_REGION  # type: ignore
        )
