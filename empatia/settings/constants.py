import datetime as dt
import os

# Model
SENSORS = ["Terra", "Aqua"]
NODATA = -9999
DEFAULT_FREQ = 470
TARGET_COL = "PM10_valor"
FEATURES_COLS = [
    "ALBEDO",
    "BCCMASS",
    "CLDHGH",
    "CLDLOW",
    "DEM_asnm",
    "valor_AOD",
    "PBLH",
    "PRECTOT",
    "PS",
    "RH",
    "SPEEDMAX",
    "SPEED",
    "T",
    "USTAR",
    "U",
    "V",
    "VIIRS_night_lights",
]

# Products
MONTHLY_PRODUCT_CODES = {"Aqua": "193000", "Terra": "163000"}

BASE_METADATA_CODES = {
    "id": "<!--mdb:mi_MI_MD_I-c-->",
    "creation_date": "<!--mdb:ii_MD_DI-ci_c-d-->",
    "band_max_value": "<!--mdb:ci_MD_CD-ag-MD_AG-a-MD_SD-max-->",
    "band_min_value": "<!--mdb:ci_MD_CD-ag-MD_AG-a-MD_SD-min-->",
    "band_max_value_2": "<!--mdb:ci_MD_CD-ag-MD_AG-a-MD_SD-max2-->",
    "band_min_value_2": "<!--mdb:ci_MD_CD-ag-MD_AG-a-MD_SD-min2-->",
}
DAILY_PM10_METADATA_CODES = {
    **BASE_METADATA_CODES,
    **{
        "modis_product_name": "<!--nombreProductoModis-->",
        "merra_product_name": "<!--NombreProductoMerra-->",
        "viirs_product_name": "<!--NombreProductoViirs-->",
    },
}
MONTHLY_PM10_METADATA_CODES = {
    **BASE_METADATA_CODES,
    **{
        "band_max_value_3": "<!--mdb:ci_MD_CD-ag-MD_AG-a-MD_SD-max3-->",
        "band_min_value_3": "<!--mdb:ci_MD_CD-ag-MD_AG-a-MD_SD-min3-->",
        "pm10_product_names": "<!--todos los productos PM10-->",
    },
}
PM10_PREFIX_FILENAME = "CONAE_MOD_CDA_ARGeoPM10_PM10"

ICA_PM10_METADATA_CODES = {
    **BASE_METADATA_CODES,
    **{"pm10_product_names": "<!--todos los productos PM10-->"},
}
ICA_PATH = "CONAE_MOD_CDA_ARGeoPM10_ICAPM10"

# ETL's
DEFAULT_DATE_FORMAT = "%Y-%m-%d"

MODIS_REGION = {"north": -21.78, "south": -55.05, "east": -53.64, "west": -73.57}

MAIAC_PRODUCT = "MCD19A2"
MAIAC_COLLECTION = 6
MAIAC_BANDS = {0: "Optical_Depth_047", 5: "AOD_QA"}


VIIRS_PRODUCT = "VNP46A1"
VIIRS_COLLECTION = 5000
VIIRS_DATE_START = f"{dt.datetime.now().year}-04-01"
VIIRS_DATE_END = f"{ dt.datetime.now().year}-06-30"
XML_VIIRS_NAME = "Promedio de Abril, Mayo y Junio  {} de VNP46A1,"


MERRA_VERSION = "5.12.4"
MERRA_REGION = ["-55.05", "-73.57", "-21.78", "-53.64"]
MERRA_BASE_URL = (
    "https://goldsmr{version}.gesdisc.eosdis.nasa.gov/daac-bin/OTF/HTTP_services.cgi"
)
MERRA_SHORTNAME = "M2I3NVASM"

MERRA_DATASETS = [
    {
        "base_url": MERRA_BASE_URL.format(version=4),
        "product": "MERRA2_400.tavg1_2d_aer_Nx",
        "shortname": "M2T1NXAER",
        "region": MERRA_REGION,
        "start_hour": "12:30:00",
        "end_hour": "20:30:59",
        "version": MERRA_VERSION,
        "variables": [
            "BCCMASS",
        ],
    },
    {
        "base_url": MERRA_BASE_URL.format(version=4),
        "product": "MERRA2_400.tavg1_2d_flx_Nx",
        "shortname": "M2T1NXFLX",
        "region": MERRA_REGION,
        "start_hour": "12:30:00",
        "end_hour": "20:30:59",
        "version": MERRA_VERSION,
        "variables": ["PBLH", "PRECTOT", "SPEED", "SPEEDMAX", "USTAR"],
    },
    {
        "base_url": MERRA_BASE_URL.format(version=4),
        "product": "MERRA2_400.tavg1_2d_rad_Nx",
        "shortname": "M2T1NXRAD",
        "region": MERRA_REGION,
        "start_hour": "12:30:00",
        "end_hour": "20:30:59",
        "version": MERRA_VERSION,
        "variables": ["ALBEDO", "CLDHGH", "CLDLOW"],
    },
    {
        "base_url": MERRA_BASE_URL.format(version=5),
        "product": "MERRA2_400.inst3_3d_asm_Nv",
        "shortname": MERRA_SHORTNAME,
        "region": MERRA_REGION,
        "start_hour": "12:00:00",
        "end_hour": "21:00:59",
        "version": MERRA_VERSION,
        "variables": ["PS", "RH", "T", "U", "V"],
    },
]

XML_MERRA_PRODUCT_NAMES = [
    "MERRA2_400.tavg1_2d_aer_Nx.{}.SUB.nc: (BCCMASS)",
    "MERRA2_400.tavg1_2d_flx_Nx.{}.SUB.nc: (PBLH, PRECTOT, SPEED, SPEEDMAX, USTAR)",
    "MERRA2_400.tavg1_2d_rad_Nx.{}.SUB.nc: (ALBEDO, CLDHGH, CLDLOW)",
    "MERRA2_400.inst3_3d_asm_Nv.{}.SUB.nc: (PS, RH, T, U, V)",
]

MIN_PERCENTAGE_OF_VALID_DATA = (
    float(os.environ.get("MIN_PERCENTAGE_OF_VALID_DATA", 0.0)) or 8.0
)
CELL_NULL_VALUE = -28672
