from typing import Dict

import requests
from requests.exceptions import HTTPError

from empatia.etl.file_writer import FileWriter
from empatia.settings.log import logger
from empatia.utils.exceptions import FileExists


def get_data(
    url: str, dst: str, file_format: str, params: Dict = {}, headers: Dict = {}
) -> None:
    """
    Download files
    Args:
        url: source url
        dst: location of the downloaded file
        file_format: file extension
        params: download parameters
        header: download header
    """
    try:
        writer = FileWriter(path=dst, file_format=file_format, force=True)
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        writer(response.content)
        logger.info(f"Contents of {response.url} written to {writer.destination}")
    except FileExists:
        logger.error("Dataset already exists")
    except HTTPError as e:
        logger.error("Data was not downloaded", exc_info=e)
        raise HTTPError
