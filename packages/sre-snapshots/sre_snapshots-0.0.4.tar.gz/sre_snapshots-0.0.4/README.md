# SERP Real Estate Snapshots Package #

A pure Python package to allow developers access to a SERP Real Estate snapshots library hosted on a NoSQL architecture.

## Installation ##

Install using pip:

```bash
pip install sre-snapshots
```

## Reading Snapshots ##

You can read snapshots by:

```python
from sre_snapshots.download_snapshots import SnapshotLibrary

library = SnapshotLibrary(
    host='127.0.0.1', 
    database_name='my_db', 
    collection_name='my_col'
)

# First 100 snapshots
snapshots = library.find_documents(
    filter_criteria={}, 
    datetime_from='2020-07-01 00:00:00',
    datetime_to='2020-07-03 23:59:59', 
    limit=10, 
    include_id=True
)

# First 100 snapshots for a specific company
snapshots_for_company = library.find_documents(
    filter_criteria={
        'matching_keyword.name': 'my_company'
    },
    datetime_from='2020-07-01 00:00:00',
    datetime_to='2020-07-03 23:59:59',
    limit=10,
    include_id=True
)

# Specific snapshot using ObjectId
specific_snapshot = library.find_documents(
    datetime_from='2020-06-01 00:00:00',
    object_id='5ee8b4814c74c3312a81b7b8'
)
```

## About the Database ##

The database is indexed on the following fields:

* ``matching_keyword.name`` (Name of the company)
* ``search_metadata.created_at`` (Date & time the search was performed)

Therefore, querying the library filtering on these fields will be very fast but filtering on any other field may be quite slow.


## Inserting New Snapshots ##

TODO: Instructions on inserting new snapshots to the database.
