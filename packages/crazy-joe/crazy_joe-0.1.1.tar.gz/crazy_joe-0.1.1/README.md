# crazy_joe

## Running Tests
```
pytest
pytest -v
pytest -v -s
```

## Build
```
python3 setup.py sdist
python3 setup.py bdist_wheel
```

## Upload
```
twine upload dist/* --verbose
```