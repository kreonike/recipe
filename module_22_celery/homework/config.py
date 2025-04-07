from datetime import timedelta

from celery import Celery
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

celery_app = Celery(
    'tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0'
)

celery_app.conf.beat_schedule = {
    'send-weekly-newsletter': {
        'task': 'celery_worker.send_newsletter_to_subscribers',
        'schedule': timedelta(weeks=1),
    },
}

subscribed_emails = set()
