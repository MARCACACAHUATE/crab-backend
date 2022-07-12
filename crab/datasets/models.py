from django.db import models
from utils.models import CrabInfoModel


class Dataset(CrabInfoModel):
    fecha_inicio = models.DateField(
            verbose_name="Fecha inicial",
            help_text="Fecha que indica el inico del dataset"
            )
    fecha_final = models.DateField(
            verbose_name="Fecha final",
            help_text="Fecha que indica el final del dataset"
            )
    user = models.ForeignKey(to="users.User", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} property"
