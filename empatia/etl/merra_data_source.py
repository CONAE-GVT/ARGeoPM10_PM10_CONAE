from datetime import datetime as dt
from typing import List
from empatia.etl.downloader import get_data
from empatia.settings import MERRA_DATASET_PATH
from empatia.settings.log import logger


def get_merra_files(
	ds: str,
	base_url: str, 
	product: str, 
	shortname: str, 
	region: List[str],
	start_hour: str, 
	end_hour: str,
	version: str,
	variables: List[str] = [],
	file_format: str = 'nc',
	) -> None:

	ds = dt.strptime(ds, "%Y-%m-%d")

	dst_path = f'{MERRA_DATASET_PATH}/{shortname}/{product}_{ds.strftime("%Y%m%d")}',
	filename = f'/data/MERRA2/{shortname}.{version}/{ds.year}/{ds.month:02d}/{product}.{ds.strftime("%Y%m%d")}.nc4'
	time = f'{ds.strftime("%Y-%m-%d")}T{start_hour}/{ds.strftime("%Y-%m-%d")}T{end_hour}'
	label = f'{product}.{ds.strftime("%Y%m%d")}.SUB.nc'

	params = {
		'FILENAME': filename,
		'FORMAT': 'bmM0Lw',
		'BBOX': ','.join(region),
		'TIME': time,
		'LABEL': label,
		'SHORTNAME': shortname,
		'SERVICE': 'L34RS_MERRA2',
		'VERSION': '1.02',
		'DATASET_VERSION': version,
		'VARIABLES': ','.join(variables)
	}

	logger.info(F'Downloading MERRA2 product: {product}')
	get_data(base_url, dst_path[0], file_format, params=params)
