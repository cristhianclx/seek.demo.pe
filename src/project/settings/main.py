# -*- coding: utf-8 -*-

from ssm_parameter_store import EC2ParameterStore

from project.settings.base import *

STAGE = "main"


##
## parameter-store
##

PARAMETER_STORE_REGION = "us-east-1"

store_ssm = EC2ParameterStore(
    region_name=PARAMETER_STORE_REGION,
)
parameters_stage = store_ssm.get_parameters_with_hierarchy("/seek.demo.pe/{}/".format(STAGE))


##
## debug
##

DEBUG = False


##
## configuration
##

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    "https://seek.demo.pe",
]


##
## templates
##

TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG


##
## databases
##

DATABASE_HOST = parameters_stage["database"]["connection"]
DATABASE_PORT = 27017
DATABASE_NAME = "bbdd"
DATABASE_USERNAME = parameters_stage["database"]["user"]
DATABASE_PASSWORD = parameters_stage["database"]["password"]
DATABASE_AUTHSOURCE = "admin"

DATABASES = {
    "default": {
        "ENGINE": "djongo",
        "NAME": DATABASE_NAME,
        "ENFORCE_SCHEMA": True,
        "CLIENT": {
            "host": DATABASE_HOST,
            "port": DATABASE_PORT,
            "username": DATABASE_USERNAME,
            "password": DATABASE_PASSWORD,
            "authSource": DATABASE_AUTHSOURCE,
        },
    }
}


##
## s3
##

DEFAULT_FILE_STORAGE = "storages.backends.s3.S3Storage"
STATICFILES_STORAGE = "storages.backends.s3.S3Storage"

AWS_S3_STATIC = "static-seek.demo.pe"

AWS_STORAGE_BUCKET_NAME = AWS_S3_STATIC

AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False

AWS_S3_FILE_OVERWRITE = False
AWS_IS_GZIPPED = True

AWS_S3_CUSTOM_DOMAIN = AWS_S3_STATIC
