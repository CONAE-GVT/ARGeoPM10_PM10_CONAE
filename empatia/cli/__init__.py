"""
    Empatia command line interface module.
"""

import click
import os
from pathlib import Path
from empatia.etl.merra_data_source import get_merra_files
from empatia.etl.modis_data_source import get_modis_files
from typing import List
from empatia.settings.log import logger


@click.group(help="Empatia: Support system for decision making in air quality management")
def main() -> None:
    """Empatia entry point script."""


@main.command(name="dump-merra-data")
@click.argument("ds", default=None, type=str)
@click.argument("base_url", default=None, type=str)
@click.argument("product", default=None, type=str)
@click.argument("shortname", default=None, type=str)
@click.argument("region", default=None, type=list)
@click.argument("start_hour", default=None, type=str)
@click.argument("end_hour", default=None, type=str)
@click.argument("version", default=None, type=str)
@click.argument("variables", default=None, type=list)
@click.argument("file_format", default="nc", type=str)
def get_merra_files_entry_point(
    ds: str,
    base_url: str, 
    product: str, 
    shortname: str, 
    region: List[str],
    start_hour: str, 
    end_hour: str,
    version: str,
    variables: List[str],
    file_format: str,
    ) -> None:

    get_merra_files(
        ds, base_url, product, shortname,
        region, start_hour, end_hour, version,
        variables, file_format
    )


@main.command(name="dump-modis-data")
@click.argument("product", default=None, type=str)
@click.argument("collection", default=None, type=int)
@click.argument("north", default=None, type=str)
@click.argument("south", default=None, type=str)
@click.argument("east", default=None, type=str)
@click.argument("west", default=None, type=str)
@click.argument("start_date", default=None, type=str)
@click.argument("end_date", default=None, type=str)
@click.argument("file_format", default="h5", type=str)
def get_modis_files_entry_point(
    product: str,
    collection: int,
    north: int,
    south: int,
    east: int,
    west: int,
    start_date: str,
    end_date: str = None,
    file_format: str = 'h5',
    ) -> None:

    get_modis_files(
        product, collection,
        north, south, east, west,
        start_date, end_date, file_format
        )

