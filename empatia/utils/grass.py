import json
from pathlib import Path
from typing import Any, List, Tuple, Union

import grass.script as grass
import grass.script.setup as gsetup
from grass.script import array as garray

from empatia.settings import GISBASE, GISDB, LOCATION, MAPSET
from empatia.settings.constants import CELL_NULL_VALUE, MIN_PERCENTAGE_OF_VALID_DATA
from empatia.settings.log import logger

_ = gsetup.init(GISBASE, GISDB, LOCATION, MAPSET)


def clean_db() -> None:
    """
    Clean GRASS DB
    """
    grass.run_command(
        "g.remove",
        pattern="*",
        exclude="viirs_*",
        type="raster,vector",
        flags="f",
    )


def raster2gtiff(rinput: str, routput: str) -> None:
    """
    Export raster map to TIFF
    Args:
        rinput: raster map name
        routput: output raster map name
    """
    grass.run_command(
        "r.out.gdal",
        input=rinput,
        output=routput + ".tif",
        type="Float64",
        flags="c",
        overwrite=True,
    )


def export_multiband_gtiff(
    raster_names: List, group_name: str, routput: str, nodata: int = -9999
) -> None:
    """
    Export raster maps to multiband TIFF
    Args:
        raster_names: raster map names
        group_name: name to create a group
        routput: output raster map name
        nodata: int to fill NaN values
    """
    grass.run_command("i.group", group=group_name, input=",".join(raster_names))
    grass.run_command(
        "r.out.gdal",
        input=group_name,
        output=routput + ".tif",
        type="Float32",
        flags="fc",
        nodata=nodata,
        overwrite=True,
    )


def raster2csv(rinput: str, routput: str) -> None:
    """
    Export raster map to CSV
    Args:
        rinput: raster map name
        routput: output raster map name
    """
    grass.run_command(
        "r.out.xyz",
        input=rinput,
        output=routput + ".csv",
        separator=",",
        overwrite=True,
    )


def raster2png(rinput: str, routput: str) -> None:
    """
    Export raster map to PNG
    Args:
        rinput: raster map name
        routput: output raster map name
    """
    grass.run_command(
        "r.out.png",
        input=rinput,
        output=routput + ".png",
        flags="t",
        overwrite=True,
    )


def set_domain(rfile: Union[str, Path]) -> None:
    """
    Set region from a given raster map
    Args:
        rfile: raster file name
    """
    grass.run_command(
        "r.in.gdal", input=rfile, output="domain", flags="e", overwrite=True
    )

    grass.run_command("g.region", raster="domain", flags="p", overwrite=True)


def get_resampling(rinput: str) -> None:
    """
    Compute bilinear resampling for a given raster map
    Args:
        rinput: raster map name
    """
    logger.info("Set resampling...")
    grass.run_command(
        "r.resamp.interp",
        input=rinput,
        output=rinput,
        method="bilinear",
        overwrite=True,
    )


def refresh_region() -> None:
    """
    Refresh region
    """
    logger.info("Refresh region...")
    grass.run_command("g.region", raster="domain", overwrite=True)


def apply_mask(raster_dir: Union[str, Path]) -> Any:
    """
    Creates a mask for limiting raster operations
    Args:
        raster_dir: vector dir path
    """
    logger.info("Applying mask...")
    grass.run_command(
        "v.in.ogr", input=raster_dir, output="mask", flags="o", overwrite=True
    )

    grass.run_command("r.mask", vect="mask", overwrite="True")
    region_data = grass.parse_command("g.region", flags="p")
    return json.loads(json.dumps(region_data))


def get_number_of_null_values(raster_name: str) -> int:
    stats_data = grass.parse_command(
        "r.stats", flags="c", sort="desc", input=raster_name, null_value=CELL_NULL_VALUE
    )

    n_of_null_values = 0
    for key in stats_data.keys():
        logger.info(f"Current key: {key}")
        if key.startswith(str(CELL_NULL_VALUE)):
            n_of_null_values = int(key.split(" ")[1])
            break

    logger.info(f"RNAME: {raster_name}")
    logger.info(f"NULLS: {n_of_null_values}")
    return n_of_null_values


def remove_mask() -> None:
    """
    Remove existing mask
    """
    grass.run_command("r.mask", flags="r")


def import_gtiff(rfile: Union[str, Path], name: str) -> None:
    """
    Import raster file (TIFF) to GRASS
    Args:
        rfile: raster file name
        name: raster map name
    """
    logger.info("Importing to gtiff...")
    grass.run_command("r.in.gdal", input=rfile, output=name, flags="o", overwrite=True)


def import_netcdf(rfile: Union[str, Path], band: int, name: str) -> None:
    """
    Import raster file (NETCDF) to GRASS
    Args:
        rfile: raster file name
        band: data index
        name: raster map name
    """
    logger.info("Importing netcdf...")
    grass.run_command(
        "r.in.gdal", input=rfile, output=name, flags="o", band=band, overwrite=True
    )


def compute_mean(rasters: List, name: str) -> None:
    """
    Compute mean for a set of raster maps
    Args:
        rasters: list of raster map names
        name: raster map name for the computed mean
    """
    grass.run_command(
        "r.series",
        input=",".join(rasters),
        method="average",
        output=name,
        overwrite=True,
    )


def compute_stddev(rasters: List, name: str) -> None:
    """
    Compute standard desviation for a set of raster maps
    Args:
        rasters: list of raster map names
        name: raster map name for the computed standard desviation
    """
    grass.run_command(
        "r.series",
        input=",".join(rasters),
        method="stddev",
        output=name,
        overwrite=True,
    )


def get_count(rasters: List, name: str) -> None:
    """
    Compute N for a set of raster maps
    Args:
        rasters: list of raster map names
        name: raster map name for the computed N
    """
    grass.run_command(
        "r.series",
        input=",".join(rasters),
        method="count",
        output=name,
        overwrite=True,
    )


def get_ranges(rinput: str) -> Tuple:
    """
    Compute Max and Min for a given raster map
    Args:
        rinput: raster map name
    Returns
        Maximum and Minimum value of the raster
    """
    raster = garray.array()
    raster.read(rinput)

    return str(raster.max()), str(raster.min())


def discretize_values(rinput: str, rule_func: Any, name: str) -> None:
    """
    Discretize values of a given raster map
    Args:
        rinput: raster map name
        rule_funct: function to assign classes
        name: discretized raster map name
    """
    raster = garray.array()
    raster.read(rinput)

    new_raster = garray.array()
    for y in range(raster.shape[0]):
        for x in range(raster.shape[1]):
            new_raster[y, x] = rule_func(raster[y, x])

    new_raster.write(mapname=f"{name}", overwrite=True)


def reset_color_table(rinput: str, rules: Union[str, Path]) -> None:
    """
    Reset color table for a given raster map
    Args:
        rinput: raster map name
        rules: file to define color table
    """
    grass.run_command(
        "r.colors",
        map=rinput,
        rules=rules,
    )


def enough_valid_data_has_been_collected(
    total_cells: int, number_of_null_cells: int
) -> bool:
    logger.info("Define if minimum amount of valid data has been collected...")
    percent_of_null_cells = number_of_null_cells * 100 / total_cells
    logger.info(f"Percent of nulls cells: {percent_of_null_cells}")
    percent_of_valid_cells = 100 - percent_of_null_cells
    logger.info(f"Percent of valid cells: {percent_of_valid_cells}")
    return percent_of_valid_cells >= MIN_PERCENTAGE_OF_VALID_DATA
