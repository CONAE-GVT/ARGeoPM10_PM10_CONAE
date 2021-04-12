# Empatia
Support system for decision making in air quality management

## Requirements
 - Python >= 3.7.0
 - Any flavour of Conda. We recommend [Miniconda](https://docs.conda.io/en/latest/miniconda.html). 


## Set up

In order to provide environment variables to the project it is needed a `.env` file in the root of the project.
Copy the `.env.template` as `.env` and replace the placeholders with real values.

```
$ cp .env.template .env
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
