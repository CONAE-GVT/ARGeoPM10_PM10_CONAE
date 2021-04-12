from typing import Dict, List, Tuple

import modapsclient

from empatia.etl.downloader import get_data
from empatia.settings import MODIS_DATASET_PATH
from empatia.settings.credentials import NASA_TOKEN
from empatia.settings.log import logger


def get_modis_urls(
    product: str,
    collection: int,
    north: float,
    south: float,
    east: float,
    west: float,
    start_date: str,
    end_date: str = None,
) -> Tuple[List[str], List[str]]:

    urls: List[str] = []
    fnames: List[Dict] = []
    mclient = modapsclient.ModapsClient()

    if not end_date:
        end_date = start_date

    try:
        # check product
        prods = mclient.listProducts()
        if not (product in prods.keys()):
            raise ValueError("Invalid product")

        # check collection
        colls = mclient.getCollections(product)
        if not str(collection) in colls.keys():
            raise ValueError(f"Invalid collection param for {product}")

        files = mclient.searchForFiles(
            product,
            start_date,
            end_date,
            north,
            south,
            east,
            west,
            collection=collection,
        )

        for fn in files:
            fnames.extend(mclient.getFileProperties(fn))
            urls.extend(mclient.getFileUrls(fn))

        prod_names: List[str] = list(
            map(lambda x: f"{product}_{x.get('fileName', '').split('.')[2]}", fnames)
        )

    except ValueError:
        logger.error(f"Invalid request to get files for {product}")
        return prod_names, urls

    return prod_names, urls


def get_modis_files(
    product: str,
    collection: int,
    north: float,
    south: float,
    east: float,
    west: float,
    start_date: str,
    end_date: str = None,
    file_format: str = "h5",
) -> None:

    headers = {"Authorization": f"Bearer {NASA_TOKEN}"}

    dst_path = (f"{MODIS_DATASET_PATH}/{product}/{start_date}/",)
    logger.info(f"Get MODIS urls to download files for: {product}")
    fnames, urls = get_modis_urls(
        product, collection, north, south, east, west, start_date, end_date
    )
    logger.info(f"Downloading MODIS's files for: {product}")
    for fn, url in zip(fnames, urls):
        get_data(url, f"{dst_path[0]}{fn}", file_format, headers=headers)
