import glob
from datetime import datetime as dt
from operator import itemgetter
from typing import Dict, List, Tuple

import gdal
import numpy as np
import rasterio
from rasterio.merge import merge
from rasterio.warp import Resampling, calculate_default_transform, reproject


def extract_modis_date(modis_date: str) -> Tuple[dt, str]:
    """
    Get sensor and date from modis format
    Args:
        modis_date: date with modis format
    Returns:
        Date and sensor type (T: Terra, A: Aqua)
    """
    sensor = ""
    if "T" in modis_date:
        date = modis_date.replace("T", "")
        sensor = "Terra"
    elif "A" in modis_date:
        date = modis_date.replace("A", "")
        sensor = "Aqua"

    # type: ignore
    date_obj: dt = dt.strptime(date, "%Y%j%H%M")

    return date_obj, sensor


def reproject_tiff(infile: str, outfile: str, dst_crs: str = "EPSG:4326") -> None:
    """
    Reproject raster map
    Args:
        infile: TIFF file
        outfile: TIFF file
        dst_crs: georeference system
    """
    with rasterio.open(infile) as src:
        transform, width, height = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds
        )
        kwargs = src.meta.copy()
        kwargs.update(
            {"crs": dst_crs, "transform": transform, "width": width, "height": height}
        )
        with rasterio.open(outfile, "w", **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.bilinear,
                )


def tag_modis_orbits(orbits: List, sensor: str) -> List:
    """
    Tag tiles
    Args:
        orbits: list of orbits
        sensor: sensor type
    Return:
        Tagged orbits
    """
    orbits = list(filter(lambda x: x[1] == sensor, orbits))
    orbits = sorted(orbits, key=itemgetter(0))

    time_th = 2700  # 2700 seg = 45 min
    init_date = orbits[0][0]
    group_tag = 1

    grouped_orbits = []
    for e in orbits:
        time_diff = e[0] - init_date
        if time_diff.seconds > time_th:
            group_tag += 1

        init_date = e[0]
        grouped_orbits.append(e + (group_tag,))

    return grouped_orbits


def groupby_sensor_by_orbit(orbits: List) -> Dict[str, List]:
    """
    Group tiles for a same orbit
    Args:
        orbits: list of orbits
        sensor: sensor type
    Return:
        Grouped orbits
    """
    res: Dict[str, List] = {}
    xs = tag_modis_orbits(orbits, "Terra")
    xs += tag_modis_orbits(orbits, "Aqua")
    for date, sensor, tile, tag in xs:
        key = f"{sensor}_{tag}"
        if key in res.keys():
            res[f"{sensor}_{tag}"].append((date, sensor, tile))
        else:
            res[f"{sensor}_{tag}"] = [(date, sensor, tile)]

    return res


def create_mosaic(tfiles: List, output_name: str) -> None:
    """
    Get mosaic from list of tiles
    Args:
        tfiles: list of tiles
        output_name: mosaic name
    """
    tiles_for_mosaic = []
    for tfile in tfiles:
        src = rasterio.open(tfile)
        tiles_for_mosaic.append(src)

    mosaic, out_trans = merge(tiles_for_mosaic)

    # write mosaic
    out_meta = src.meta.copy()
    out_meta.update(
        {
            "driver": "GTiff",
            "height": mosaic.shape[1],
            "width": mosaic.shape[2],
            "transform": out_trans,
        }
    )

    with rasterio.open(output_name, "w", **out_meta) as f:
        f.write(mosaic)


def modis_hdf_2_tiff(
    infile: str,
    subset: int,
    prefix_outfile: str,
    outdir: str = "",
    non_value: int = -32768,
) -> List:
    """
    Get Modis layers from HDF file
    Args:
        infile: HDF file
        subset: product index
        prefix_outfile: prefix for output file
        outdir: ouput directory
        non_value: int to fill missing values
    Return:
        List of orbits for the given subset
    """
    hdf_ds = gdal.Open(infile, gdal.GA_ReadOnly)
    band_ds = gdal.Open(hdf_ds.GetSubDatasets()[subset][0], gdal.GA_ReadOnly)

    # read metadata
    metadata = band_ds.GetMetadata_Dict()
    orbits = metadata.get("Orbit_time_stamp", "").split(" ")
    orbits = list(filter(lambda x: x != "", orbits))
    htile = metadata.get("HORIZONTALTILENUMBER", "")
    vtile = metadata.get("VERTICALTILENUMBER", "")
    tile = f"h{htile}_v{vtile}"

    # read into numpy array
    band_array = band_ds.ReadAsArray().astype(np.int16)

    # convert no_data values
    band_array[band_array == -28672] = non_value

    # write raster
    bands = []
    for e, orbit in enumerate(orbits):
        date, sensor = extract_modis_date(orbit)
        orbit_outfile = f"{outdir}{prefix_outfile}_{date.hour}_{sensor}_{tile}.tif"
        out_ds = gdal.GetDriverByName("GTiff").Create(
            orbit_outfile,
            band_ds.RasterXSize,
            band_ds.RasterYSize,
            1,  # Number of bands
            gdal.GDT_Int16,
            ["COMPRESS=LZW", "TILED=YES"],
        )
        out_ds.SetGeoTransform(band_ds.GetGeoTransform())
        out_ds.SetProjection(band_ds.GetProjection())
        out_ds.GetRasterBand(1).WriteArray(band_array[e])
        out_ds.GetRasterBand(1).SetNoDataValue(non_value)

        out_ds = None  # close dataset to write to disc
        reproject_tiff(orbit_outfile, orbit_outfile)
        bands.append((date, sensor, tile))

    return bands


def get_modis_mosaic(indir: str, band: int, prefix: str, outdir: str = "") -> List:
    """
    Create mosaics for each orbit of a given band
    Args:
        indir: directory of HDF tiles
        band: product index
        prefix: prefix of the output file
        outdir: directory of the output file
    Return
        List of generated mosaic metadata
    """
    if outdir == "":
        outdir = indir

    rfiles = sorted(glob.glob(f"{indir}*.hdf"))
    bands = []
    for rfile in rfiles:
        bands.extend(modis_hdf_2_tiff(rfile, band, prefix, indir))

    orbit_groups = groupby_sensor_by_orbit(bands)

    # generate mosaics
    mosaic_files = []

    for key, tiles in orbit_groups.items():
        if len(tiles) > 2:
            date = tiles[0][0]
            sensor = tiles[0][1]
            if (date.hour >= 12) and (date.hour <= 20):
                tfiles = sorted(glob.glob(f"{indir}{prefix}_{date.hour}_{sensor}*.tif"))
                output_name = f"{outdir}{prefix}_{date.hour}_{sensor}.tif"
                create_mosaic(tfiles, output_name)
                mosaic_files.append(
                    {"file": output_name, "sensor": sensor, "date": date}
                )

    return mosaic_files


def viirs_hdf_2_tiff(
    infile: str,
    subset: int,
    outdir: str,
    non_value: int = -9999,
) -> None:
    """
    Get VIIRS layers from HDF file
    Args:
        infile: HDF file
        subset: product index
        outdir: ouput directory
        non_value: int to fill missing values
    """
    EPSG = "-a_srs EPSG:4326"  # WGS84

    # read hdf subset
    hdflayer = gdal.Open(infile, gdal.GA_ReadOnly)
    subhdflayer = hdflayer.GetSubDatasets()[subset][0]
    rlayer = gdal.Open(subhdflayer, gdal.GA_ReadOnly)

    # collect bounding box coordinates
    htile_number = int(rlayer.GetMetadata_Dict()["HorizontalTileNumber"])
    vtile_number = int(rlayer.GetMetadata_Dict()["VerticalTileNumber"])

    west_bound = (10 * htile_number) - 180
    north_bound = 90 - (10 * vtile_number)
    east_bound = west_bound + 10
    south_bound = north_bound - 10

    outfile = f"{outdir}viirs_{htile_number}_{vtile_number}.tif"

    # translate format
    option_text = (
        f"{EPSG} -a_ullr {west_bound} {north_bound} {east_bound} {south_bound}"
    )
    translate_opt = gdal.TranslateOptions(gdal.ParseCommandLine(option_text))
    gdal.Translate(outfile, rlayer, options=translate_opt, noData=non_value)


def get_viirs_mosaic(path: str, band: int, outdir: str, outname: str) -> None:
    """
    Create mosaics for a given VIIRS band
    Args:
        indir: directory of HDF tiles
        band: product index
        outdir: directory of the output file
        outname: output file name
    """
    # translate format
    rfiles = sorted(glob.glob(f"{path}/*.h5"))
    for rfile in rfiles:
        output_name = f"{rfile}.tif"
        viirs_hdf_2_tiff(rfile, band, path)

    # generate mosaic
    tiles_for_mosaic = []
    tfiles = sorted(glob.glob(f"{path}/*.tif"))
    for tfile in tfiles:
        src = rasterio.open(tfile)
        tiles_for_mosaic.append(src)

    mosaic, out_trans = merge(tiles_for_mosaic)

    # write mosaic
    out_meta = src.meta.copy()
    out_meta.update(
        {
            "driver": "GTiff",
            "height": mosaic.shape[1],
            "width": mosaic.shape[2],
            "transform": out_trans,
        }
    )
    output_name = f"{outdir}{outname}"
    with rasterio.open(output_name, "w", **out_meta) as f:
        f.write(mosaic)
