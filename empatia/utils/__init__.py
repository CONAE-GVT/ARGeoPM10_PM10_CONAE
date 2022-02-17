import os
import glob
import numpy as np
import datetime as dt
import shutil
from pathlib import Path
from typing import Dict, List, Union
from empatia.settings.constants import DEFAULT_DATE_FORMAT


def date_range(start: dt.date, end: dt.date) -> List[str]:
    delta = end - start
    date_list = []
    for i in range(delta.days + 1):
        day = start + dt.timedelta(days=i)
        date_list.append(day.strftime(DEFAULT_DATE_FORMAT))

    return date_list


def get_qa_class(x: float) -> int:
    _class = -9999
    if np.isnan(x):
        _class = -9999
    elif (x > 0.1) and (x <= 54):
        _class = 1
    elif (x > 54) and (x <= 154):
        _class = 2
    elif (x > 154) and (x <= 254):
        _class = 3
    elif (x > 254) and (x <= 354):
        _class = 4
    elif (x > 354) and (x <= 424):
        _class = 5
    elif x > 424:
        _class = 6

    return _class


def create_xml(xml_template: Union[str, Path], metadata: Dict, outfile: str) -> None:

    with open(xml_template, "r") as xml_file:
        xml = "".join(xml_file.readlines())

    for key, value in metadata.items():
        xml = xml.replace(key, value)

    with open(f"{outfile}.xml", "w") as xml_file:
        xml_file.writelines(xml)


def zip_directory(input_dir: str, output_dir: str) -> None:
    shutil.make_archive(output_dir, "zip", input_dir)


def remove_folder(path: str) -> None:
    if os.path.exists(path):
        shutil.rmtree(path)
    else:
        print(f"Folder not found: {path}")


def remove_folders_from_date(pattern: str, ds: dt.date) -> None:
    paths = sorted(glob.glob(pattern))
    for path in paths:
        path_ds = dt.datetime.strptime(path.split("/")[-1], DEFAULT_DATE_FORMAT)
        if path_ds < ds:
            remove_folder(path)


def remove_file(path: str) -> None:
    if os.path.exists(path):
        os.remove(path)
        print(f"Deleted file: {path}")
    else:
        print(f"No {path} file to delete")
