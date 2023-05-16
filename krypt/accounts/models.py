from django.db import models

from django.contrib.auth.models import AbstractUser

class UserModel(AbstractUser):

    Ethaddress = models.CharField(max_length=255 , default='NA')
    Ethprivatekey = models.CharField(max_length=255 , default='NA')

    def __str__(self):
        return self.username


