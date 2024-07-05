# -*- coding: utf-8 -*-

###
### gunicorn WSGI server configuration
###

from multiprocessing import cpu_count


def max_workers():
    return cpu_count() + 1


reload = True
chdir = "/home/cristhian/code/"

name = "gunicorn"
pythonpath = "/home/cristhian/code/project/"
bind = "0.0.0.0:5000"
loglevel = "error"

limit_request_line = 0
max_requests = 1000
worker_class = "gevent"
workers = max_workers()

timeout = 300
