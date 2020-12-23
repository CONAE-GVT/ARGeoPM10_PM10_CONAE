# Empatia
Support system for decision making in air quality management

# Development
- Install requirements: `pip install -r requirements-dev.txt`
- Install pre-commit `pre-commit install`
- Add pre-push hook `touch .git/hooks/pre-push;echo "pytest && mypy .\nexit \$?" > .git/hooks/pre-push; chmod a+x .git/hooks/pre-push`
