web: gunicorn challengesite.wsgi --log-file -
release: python manage.py migrate
worker: celery -A challengesite worker --loglevel=info --concurrency=1