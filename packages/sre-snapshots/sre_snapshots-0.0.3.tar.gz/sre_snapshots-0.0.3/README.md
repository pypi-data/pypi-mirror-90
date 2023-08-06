# SERP Real Estate Snapshots Package #

The package is currently hosted on TestPyPi: https://test.pypi.org/project/sre-snapshots/.

## Using this Package ##

Install using pip:

```bash
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple sre-snapshots==0.0.3
```

## Updating this Package ##

Update ``setup.py`` to a new version if necessary.

```bash
python setup.py sdist bdist_wheel
python -m twine upload --repository-url https://test.pypi.org/legacy/ --skip-existing dist/*
```

## About the Database ##

Indexing = fast querying

## Project Structure ##

This package contains functions for reading and inserting snapshots into the SERP Real Estate NoSQL database.

## Reading Snapshots ##

You can read snapshots by:

```python
from sre_snapshots.download_snapshots import SnapshotLibrary

library = SnapshotLibrary(host=str('35.214.82.10'))

# First 100 snapshots
snapshots = library.find_documents(
    filter_criteria={}, 
    datetime_from=str('2020-07-01 00:00:00'), 
    datetime_to=str('2020-07-03 23:59:59'), 
    limit=10, 
    include_id=True
)

# Specific snapshot using ObjectId
specific_snapshot = library.find_documents(
    datetime_from=str('2020-06-01 00:00:00'),
    object_id=str('5ee8b4814c74c3312a81b7b8')
)
```

## Inserting New Snapshots ##

TODO: Instructions on inserting new snapshots to the database.

## Unit Testing ##

All unit tests are in the ``tests/`` directory.

To run all tests using the CLI (using [Test Discovery](https://docs.python.org/3/library/unittest.html#unittest-test-discovery)):

```bash
python -m unittest discover -s tests -v
``` 

Or to run a specific test module:

```bash
python -m unittest tests/test_date_funs.py -v
```
