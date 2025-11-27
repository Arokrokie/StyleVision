web: python startup.py && gunicorn hair_project.wsgi --bind 0.0.0.0:$PORT --workers 1 --timeout 300 --max-requests 100 --preload --log-level info
