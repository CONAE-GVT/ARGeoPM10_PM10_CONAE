"""
    Empatia command line interface module.
"""

import click
from empatia.cli.pipelines import (
    viirs_etl,
    daily_pipeline,
    clean_storages,
    monthly_pipeline,
)
from empatia.cli.training import train


@click.group(
    help="Empatia: Support system for decision making in air quality management"
)
def main() -> None:
    """Empatia entry point script."""


@main.command(name="hello")
def hello_world() -> None:
    print("Hello Empatia!")


@main.command(name="run_viirs_etl")
def run_viirs_etl() -> None:
    viirs_etl()


@main.command(name="compute_daily_products")
@click.option("--start-date", "start_date", type=str)
@click.option("--end-date", "end_date", type=str)
def compute_daily_products(start_date: str, end_date: str) -> None:
    daily_pipeline(start_date, end_date)


@main.command(name="compute_monthly_products")
@click.option(
    "--ndays",
    default=30,
    type=int,
    help="Number of before days to start monthly process",
)
def compute_monthly_products(ndays: int) -> None:
    monthly_pipeline(ndays)


@main.command(name="clean_all")
@click.option(
    "--ndays",
    default=60,
    type=int,
    help="Number of before days to start the cleaning",
)
def clean_all(ndays: int) -> None:
    clean_storages(ndays)


@main.command(name="run_training")
def run_training() -> None:
    train()
