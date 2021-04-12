# Empatia
Support system for decision making in air quality management

## Development
- Install requirements: `pip install -r requirements-dev.txt`
- Install pre-commit `pre-commit install`
- Add pre-push hook `touch .git/hooks/pre-push;echo "pytest && mypy .\nexit \$?" > .git/hooks/pre-push; chmod a+x .git/hooks/pre-push`


## Set up

### Create a .netrc file in your home directory

Locate `$HOME` directory
```
$ cd $HOME
```

Create `.netrc` file
```
$ touch .netrc
```

Write credentials, where `<uid>` is your user name and `<password>` is your Earthdata Login password without the brackets.
```
$ echo "machine urs.earthdata.nasa.gov login <uid> password <password> >> .netrc"
```


Change the permissions
```
chmod 0600 .netrc 
```