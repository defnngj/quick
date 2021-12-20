# quick


uwsgi --http-socket :8002 --chdir /home/app/quick/backend --wsgi-file backend/wsgi.py --master --processes 4 --threads 2