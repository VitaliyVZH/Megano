import os

bind = 'unix:/run/gunicorn.sock'
workers = 3
worker_class = 'gevent'
timeout = 60
keepalive = 2
loglevel = 'info'
capture_output = True
logfile = '/var/log/gunicorn/gunicorn.log'
chdir = '/app'
user = 'nginx'
umask = 0o007