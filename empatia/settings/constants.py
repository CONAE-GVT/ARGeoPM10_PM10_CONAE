import datetime as dt

DEFAULT_DATE = dt.datetime.now() - dt.timedelta(days=1)

MODIS_REGION = {"north": -21.76, "south": -55.08, "east": -53.58, "west": -73.6}

MAIAC_PRODUCT = "MCD19A2"
MAIAC_COLLECTION = 6


VIIRS_PRODUCT = "VNP46A1"
VIIRS_COLLECTION = 5000


MERRA_VERSION = "5.12.4"
MERRA_REGION = ["-55.08", "-73.6", "-21.76", "-53.58"]
MERRA_BASE_URL = (
    "https://goldsmr{version}.gesdisc.eosdis.nasa.gov/daac-bin/OTF/HTTP_services.cgi"
)

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
            "DMSSMASS",
            "DUSMASS",
            "OCSMASS",
            "SO2SMASS",
            "SO4SMASS",
            "SSSMASS",
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
        "shortname": "M2I3NVASM",
        "region": MERRA_REGION,
        "start_hour": "12:00:00",
        "end_hour": "21:00:59",
        "version": MERRA_VERSION,
        "variables": ["PS", "RH", "T", "U", "V"],
    },
]
