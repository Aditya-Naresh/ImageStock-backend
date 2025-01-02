from celery import shared_task
from .utils import send_normal_email
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from .models import User
import environ

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_verification_email(self, user_id):
    print("Send verification email:")
    FRONTEND = env("FRONTEND")

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return

    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_link = f"{FRONTEND}/verify-email/{uid}/{token}"
    message = f"""
        Hi {user.name},
        Please click the link below to verify your email address:
        {verification_link}
        If you did not request this, please ignore this email.
        Thank you!
    """

    data = {
        "email_subject": "Verification Mail",
        "email_body": message,
        "from_email": settings.EMAIL_HOST_USER,
        "to_email": user.email,
    }
    print(data)
    try:
        send_normal_email(data)
    except Exception as e:
        self.retry(exc=e)
        print(f"Error sending email: {e}")

