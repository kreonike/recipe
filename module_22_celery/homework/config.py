from datetime import timedelta

from celery import Celery

celery_app = Celery(
    'tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0'
)

celery_app.conf.beat_schedule = {
    'send-weekly-newsletter': {
        'task': 'celery_worker.send_newsletter_to_subscribers',
        'schedule': timedelta(weeks=1),
    },
}

SMTP_HOST = "smtp.yandex.com"
SMTP_PORT = 587
SMTP_USER = "your_email@yandex.com"
SMTP_PASSWORD = "your_password_or_app_token"

subscribed_emails = set()
