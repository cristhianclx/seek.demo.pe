#!/usr/bin/env python

import os
import sys

import pytest

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    sys.exit(pytest.main())
