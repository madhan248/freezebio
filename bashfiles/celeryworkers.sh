# cd project/freezebio

# cd ..
source venv/bin/activate
celery --app freezebio worker -l info