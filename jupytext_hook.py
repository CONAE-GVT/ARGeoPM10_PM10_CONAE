import sys
from pathlib import Path

import jupytext

nbfile = Path(sys.argv[1])
mdfile = str(nbfile.with_suffix(".md"))

nb = jupytext.read(open(nbfile), fmt="ipynb")
jupytext.write(nb, mdfile, fmt="md")
