from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    date_of_birth = models.DateTimeField(verbose_name = "Date Of Birth", null=True, blank=True)
    address = models.TextField(verbose_name="Address of User", null=True, blank=True)

    def __str__(self) -> str:
        return self.address
