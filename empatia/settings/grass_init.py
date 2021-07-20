import os
import sys
from typing import Tuple


def grass_setup() -> Tuple[str, str, str, str]:
    """
    Get GRASS configuration
    """
    # DATA
    # Define GRASS DATABASE
    # Add your path to grassdata (GRASS GIS database) directory
    gisdb = os.path.join(os.path.expanduser("~"), "grass")
    # Set GISDBASE environment variable
    os.environ["GISDBASE"] = gisdb
    # Specify (existing) location and mapset
    location = "LatLon"
    mapset = "empatia"
    # Query GRASS 7 itself for its GISBASE
    gisbase = "/usr/lib/grass78"
    # Set GISBASE environment variable
    os.environ["GISBASE"] = gisbase
    # The following not needed with trunk
    os.environ["PATH"] += os.pathsep + os.path.join(gisbase, "extrabin")

    # Define GRASS-Python environment
    gpydir = os.path.join(gisbase, "etc", "python")
    sys.path.append(gpydir)

    return gisbase, gisdb, location, mapset
