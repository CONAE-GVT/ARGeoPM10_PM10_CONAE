from pathlib import Path

# Local paths
BASE_PATH = Path(__file__).resolve().parent.parent  # Root of the package

DATASET_PATH = BASE_PATH.parent / "data"
MODIS_DATASET_PATH = DATASET_PATH / "modis"
MERRA_DATASET_PATH = DATASET_PATH / "merra"
