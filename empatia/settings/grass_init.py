import os
import sys
from typing import Tuple


def grass_setup() -> Tuple[str, str, str, str]:
    """
    Get GRASS configuration
    """
    gisdb = os.environ["GISDBASE"]
    location = os.environ["LOCATION"]
    mapset = os.environ["MAPSET"]
    gisbase = os.environ["GISBASE"]
    # The following not needed with trunk
    os.environ["PATH"] += os.pathsep + os.path.join(gisbase, "extrabin")

    # Define GRASS-Python environment
    gpydir = os.path.join(gisbase, "etc", "python")
    sys.path.append(gpydir)

    return gisbase, gisdb, location, mapset
