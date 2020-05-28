python manage.py db upgrade
uwsgi --http 0.0.0.0:5000 --wsgi-file ./manage.py --callable app --threads 40 --enable-threads