bind = '127.0.0.1:8081'
workers = 2

# ! gunicorn -c gunicorn/g.conf.py askme_kulinich.wsgi:application