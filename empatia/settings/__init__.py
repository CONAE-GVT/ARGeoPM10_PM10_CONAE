from pathlib import Path
from .grass_init import grass_setup

# Local paths
BASE_PATH = Path(__file__).resolve().parent.parent  # Root of the package

DATASET_PATH = BASE_PATH.parent / "data"
MODIS_DATASET_PATH = DATASET_PATH / "modis"
MERRA_DATASET_PATH = DATASET_PATH / "merra"
PREDICTION_DATA_PATH = DATASET_PATH / "predict"
PROCESSED_DATA_PATH = DATASET_PATH / "processed"
MODEL_DATA_PATH = DATASET_PATH / "model"
MODEL_PATH = MODEL_DATA_PATH / "model_2021-05-13.pkl"  # "pm10_random_forest.pkl"
TRAINING_DATA_PATH = MODEL_DATA_PATH / "training_dataset.csv"

GISBASE, GISDB, LOCATION, MAPSET = grass_setup()
REGION_DATA_PATH = DATASET_PATH / "region"
DOMAIN_DATA_PATH = REGION_DATA_PATH / "DEM_asnm.tif"

UTILS_PATH = DATASET_PATH / "utils"
DAILY_PM10_TEMPLATE_PATH = UTILS_PATH / "PM10basev1.xml"
MONTHLY_T_PM10_TEMPLATE_PATH = UTILS_PATH / "PM10mMbasev1.xml"
MONTHLY_A_PM10_TEMPLATE_PATH = UTILS_PATH / "PM10mVbasev1.xml"
ICA_TEMPLATE_PATH = UTILS_PATH / "ICAPM10basev1.xml"
PM10_COLOR_RULES_PATH = UTILS_PATH / "pm10_color_rules.txt"
ICA_COLOR_RULES_PATH = UTILS_PATH / "ica_color_rules.txt"


MONTHLY_PRODUCT_TEMPLATES = {
    "Aqua": MONTHLY_A_PM10_TEMPLATE_PATH,
    "Terra": MONTHLY_T_PM10_TEMPLATE_PATH,
}
