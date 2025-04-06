import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import (
    celery_app,
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USER,
    SMTP_PASSWORD,
    subscribed_emails,
)
from mail import send_email


@celery_app.task
def process_image(image_path, order_id, email):
    try:
        from image import blur_image
        import os

        blurred_filename = f"blurred_{os.path.basename(image_path)}"
        blur_image(image_path, blurred_filename)

        send_email(order_id, email, blurred_filename)

        os.remove(blurred_filename)
        return True
    except Exception as e:
        print(f"Error processing image: {e}")
        return False


@celery_app.task
def send_newsletter(email):
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)

            email_msg = MIMEMultipart()
            email_msg['Subject'] = 'Weekly Newsletter from Image Processing Service'
            email_msg['From'] = SMTP_USER
            email_msg['To'] = email

            text = "Thank you for using our image processing service! Here's your weekly update."
            email_msg.attach(MIMEText(text, 'plain'))

            server.sendmail(SMTP_USER, email, email_msg.as_string())
        return True
    except Exception as e:
        print(f"Error sending newsletter: {e}")
        return False


@celery_app.task
def send_newsletter_to_subscribers():
    for email in subscribed_emails:
        send_newsletter.delay(email)
