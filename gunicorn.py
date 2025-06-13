# -*- coding: utf-8 -*-
import multiprocessing

pidfile = 'gunicorn.pid'
errorlog = 'logs/gunicorn-error.log'
accesslog = 'logs/gunicorn-access.log'
access_log_format = "%(h)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s %({Body}i)s %({Body}o)s"
loglevel = 'DEBUG'
bind = '0.0.0.0:5151'
daemon = False
# Better performance (2*CPU)+1
#workers = multiprocessing.cpu_count() * 2 + 1
workers = 50
