# Empatia
Support system for decision making in air quality management

## Requirements
 - Python >= 3.7.0
 - GRASS GIS >= 7.6
 - Any flavour of Conda. We recommend [Miniconda](https://docs.conda.io/en/latest/miniconda.html).
 - A version Docker on your OS


## Local Set up

In order to provide environment variables to the project it is needed a `.env` file in the root of the project.
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
$ echo "machine urs.earthdata.nasa.gov login <uid> password <password> >> .netrc"
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
./tools/install_common_tools.sh
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
$ ./commands/build.sh --tag <tag_name>
```

- Create container
```
$ docker run --name <container_name> --env-file .env-docker -it empatia:<tag_name> /bin/bash
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
```

```
$ touch .netrc
```

```
$ echo "machine urs.earthdata.nasa.gov login <uid> password <password> >> .netrc"
```
where `<uid>` is your user name and `<password>` is your Earthdata Login password without the brackets.

```
chmod 0600 .netrc
```

## CLIs

```
$ empatia run_viirs_etl
```

It runs pipeline to get the mean of April, May and June of the product `VNP46A1`.

```
$ empatia compute_daily_products
```

It runs pipeline to get  the following daily products:
* PM10 and QA_AOD per sensor orbit
* ICA PM10

for the current date and tries to get these missing products for previous days.

```
$ empatia compute_monthly_products --ndays 30
```

It runs pipeline to get the following monthly statisticians:
* Mean
* Standar Desviation
* N

from the given predictions for the month of: `current date - ndays`

```
$ empatia clean_all --ndays 60
```

It cleans GRASS DB and removes obsolete files/folder created before `current date - ndays`

```
$ empatia run_training
```

It runs PM1O model training


## How to set custom color palletes

* If you want to change the PM10 color pallete, you need to change the following file: `empatia/data/utils/pm10_color_rules.txt`.
This file looks like:
```
    0.1 0:0:255
    0.5 0:128:255
    1 0:255:255
    3 128:255:0
    5 255:255:0
    10 255:128:0
    20 255:0:0
    50 255:0:128
    100 255:0:255
    200 128:0:255
```
where the first column is the PM10 value and the second column is the RGB color.


* If you want to change the ICA color pallete, you need to change the following file: `empatia/data/utils/ica_color_rules.txt`.
This file looks like:
```
    1 39:174:96
    2 46:204:113
    3 241:196:15
    4 230:126:34
    5 231:76:60
    6 192:57:43
```
where the first column is the ICA value and the second column is the RGB color.
