import os
import datetime as dt
from typing import List
from empatia.settings.constants import DEFAULT_DATE
from empatia.settings.log import logger


def date_range(start: dt.date, end: dt.date) -> List[str]:
	delta  = end - start
	date_list = []
	for i in range(delta.days + 1):
		day = start + dt.timedelta(days=i)
		date_list.append(day.strftime("%Y-%m-%d"))

	return date_list


def retrieve_dates(source: str, product: str, file_format: str = None) -> List[str]:
	default_ft = "%Y-%m-%d"
	path = f"{source}/{product}"
	logger.info(f"Retrieve date for: {product}")
	datasets = sorted(filter(lambda x: not x.startswith('.'), os.listdir(path)))

	recovery_dates = [DEFAULT_DATE.strftime(default_ft)]
	if datasets:
		last_date = datasets[-1]
		last_date = dt.datetime.strptime(last_date, default_ft)
		recovery_dates = date_range(start=last_date, end=DEFAULT_DATE)

	return recovery_dates







