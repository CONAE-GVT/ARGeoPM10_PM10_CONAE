# Project Structure

Here is the basic skeleton for `empatia` app repo:

```bash
├── commands                        # contains bash files to install common tools and build Docker images.
├── empatia                         # main app directory.
│   ├── cli                         	# contains modules to execute Python commands.
│   ├── etl                         	# contains modules to define an ETL.
│   ├── models                      	# contains modules to implement models.
│   ├── settings                    	# contains modules to define all necessary settings.
│   └── utils                    	    # contains modules to define all util/common functions.
├── data                            # contains data files used in the project.
├── Dockerfile                      # contains all the commands that we want to execute on the command line to build an image.
├── docker_entrypoint.sh            # specifies the executable that the container will use.
├── data                            # contains data files used in the project.
├── jupyter_hook.py                 # converts ipynb (notebooks) files to Markdown file
├── notebooks                       # contains experimental files.
├── PROJECT_STRUCTURE.md            # overview of the project structure.
├── README.md                       # overview of the project.
├── requirements.txt                # Python required libraries.
├── requirements-dev.txt            # Python required libraries for development.
├── setup.py                        # specifies which modules/packages are about to be installed.
└── .gitignore                      # specifies intentionally untracked files that Git should ignore.
```