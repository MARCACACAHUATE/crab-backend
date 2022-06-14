from django.db import models
from django.contrib.auth.models import AbstractUser

from utils.models import CrabInfoModel

class User(CrabInfoModel, AbstractUser):
    
    email = models.EmailField(
        verbose_name = "correo",
        unique = True,
        error_messages = {
            'unique': "Este correo ya esta en uso"
        }
    )
    is_verified = models.BooleanField(
        verbose_name = "verificado",
        default = False,
        help_text = "Cambia a True cuando el usuario verifica su correo"
    )
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.username