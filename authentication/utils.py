from django.conf import settings
from django.core.mail import EmailMessage, BadHeaderError
from smtplib import SMTPException
import environ

env = environ.Env(DUBUG=(bool, False))
environ.Env.read_env()


def send_normal_email(data):
    try:
        email = EmailMessage(
            subject=data["email_subject"],
            body=data["email_body"],
            from_email=settings.EMAIL_HOST_USER,
            to=[data["to_email"]],
        )
        email.send(fail_silently=False)
        print("Email send successfully to user")
    except BadHeaderError:
        print("Invalid header found when sending email")
    except SMTPException as e:
        print("SMTPException occured: %s", e)
    except Exception as e:
        print("An unexpected error occured: ", e)
