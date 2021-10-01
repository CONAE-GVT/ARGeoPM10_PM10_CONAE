# Empatia
Support system for decision making in air quality management

## Requirements
 - Python >= 3.7.0
 - GRASS GIS >= 7.6 (GRASS GIS should be updated to >= 7.8, though it is not yet tested for this implementation)
 - Any flavour of Conda. We recommend [Miniconda](https://docs.conda.io/en/latest/miniconda.html).
 - A version Docker on your OS


## Local Set up

In order to provide environment variables to the project, it is needed a `.env` file in the root of the project.
Copy the `.env.template` as `.env` and replace the placeholders with real values.

```
$ cp .env.template .env
```

```
$ export $(xargs < .env)
```

Create a .netrc file in your home directory.
```
$ cd $HOME
```

```
$ touch .netrc
```

```
$ echo "machine urs.earthdata.nasa.gov login <uid> password <password>" >> .netrc
```
where `<uid>` is your user name and `<password>` is your Earthdata Login password without the brackets.

```
chmod 0600 .netrc 
```

Generate the Conda environment and install all the dependencies.
```
$ conda create -n <environment name> python=3.7
```

```
$ conda activate <environment name>
```

```
$ pip install -r requirements-dev.txt
```

Also, you can install common tools running the following script:
```
./commands/install_common_tools.sh
```

Once your Git Repository was set, install the local hooks.
- Install pre-commit
```
$ pre-commit install
```

- Add pre-push hook
```
$ touch .git/hooks/pre-push;echo "pytest" > .git/hooks/pre-push; chmod a+x .git/hooks/pre-push
```

## Dockerized App

- Build image
```
$ ./commands/build_docker_image.sh --tag <tag_name>
```

- Create and run container
```
$ docker run --name <container_name> --env-file .env -it empatia:<tag_name> /bin/bash
```

- Create and run container defining new environment variables
```
echo "MIN_PERCENTAGE_OF_VALID_DATA=8.0" >> .env
$ docker run --name <container_name> --env-file .env -it empatia:<tag_name> /bin/bash
```

- Run container
```
$ docker start <container_name>
```

- Enter to container
```
$ docker exec -it <container_name> /bin/bash
```

 - Create a .netrc file in home directory.
```
$ cd
$ touch .netrc
```

```
$ echo "machine urs.earthdata.nasa.gov login <uid> password <password> >> .netrc"
```
where `<uid>` is your user name and `<password>` is your Earthdata Login password without the brackets.

```
chmod 0600 .netrc

```

- Run daily_pipeline in container
```
cd $HOME
touch conae.logs
$ docker exec -it <container_name> empatia compute_daily_products > $HOME/conae.logs
```



## Get the model file

To run the model in your own working station or server, you should obtain the model file from the next FTP access:

```
FTP: ftp4.conae.gov.ar/prod11/
username: daye
password: dE#2810
```

Download the `model_2021-05-13.pkl` file and save it into the `./data/model/` directory.


## CLIs

```
$ empatia run_viirs_etl
```

It runs pipeline to get the nocturne ligths mean of April, May and June from the `VNP46A1` daily dataset.

```
$ empatia compute_daily_products
```

It runs pipeline to get  the following daily products:
* PM10 and QA_AOD per sensor and orbit.
* ICA PM10 (daily air quality index from PM10).

for the current date and other missing data for previous days.

```
$ empatia compute_monthly_products --ndays 30
```

It runs pipeline to get the following monthly statistics:
* Monthly Mean
* Monthly Standard Deviation
* Monthly N data considered

from the given predictions for the month of: `current date - ndays`.

```
$ empatia clean_all --ndays 60
```

It cleans GRASS DB and removes obsolete files/folder created before `current date - ndays`.

```
$ empatia run_training
```

It runs PM1O model training.


## How to set custom color scale for PNG files

* If you want to change the PM10 color scale, change the following file: `empatia/data/utils/pm10_color_rules.txt`.
This file looks like:
```
    50 26:150:65
    75 166:217:106
    100 255:255:192
    125 253:174:97
    150 215:25:28
```
where the first column is the PM10 value and the second column is the RGB color.


* If you want to change the ICA color scale, you need to change the following file: `empatia/data/utils/ica_color_rules.txt`.
This file looks like:
```
    1 0:228:0
    2 255:255:0
    3 255:126:0
    4 255:0:0
    5 143:63:151
    6 126:0:35
```
where the first column is the ICA value and the second column is the RGB color. These definitions are taken from US Environmental Protection Agency (2018), Technical Assistance Document for the Reporting of Daily Air Quality – the Air Quality Index (AQI), EPA-454/B-18-007 (https://www.airnow.gov/sites/default/files/2020-05/aqi-technical-assistance-document-sept2018.pdf).
