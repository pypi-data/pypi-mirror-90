# Object Oriented Modelling Framework for Causal Models

# Installing from pip
```
pip install oomodelling
```

# Installing the package from source code

Open terminal in this folder.

```
pip install -e .
```

# Publishing this package on pypi

Activate virtual environment and:
```
python setup.py sdist
python setup.py bdist_wheel
python -m twine upload dist/*
set user and password according to pypi's api token
```

## Common Issues

Error:
```
error: invalid command 'bdist_wheel'
```
Solution:
```
pip install wheel
```