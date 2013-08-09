#!/bin/bash

python manage.py loaddata formats.json
python manage.py loaddata organizations.json
python manage.py loaddata scientists.json
python manage.py loaddata datacatalogs.json
python manage.py loaddata datasets.json
