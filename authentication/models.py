from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    def create_user(
        self,
        email,
        phone_number,
        password=None,
        **extra_fields,
    ):
        if not email:
            raise ValueError("The Email is required")
        if not phone_number:
            raise ValueError("The Phone Number is required")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            phone_number=phone_number,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        phone_number,
        password=None,
        **extra_fields,
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_verified", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True")
        if not extra_fields.get("is_admin"):
            raise ValueError("Superuser must have is_admin=True")

        return self.create_user(email, phone_number, password, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(unique=True)
    name = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    objects = CustomUserManager()

    REQUIRED_FIELDS = ["phone_number"]
    USERNAME_FIELD = "email"

    def __str__(self):
        return f"{self.pk} : {self.email}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
