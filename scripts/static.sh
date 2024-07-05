#!/bin/bash

mkdir -p src/static-files/
chmod -R 755 src/static-files/

cp -r src/static/* src/static-files/

python src/manage.py collectstatic --no-input
