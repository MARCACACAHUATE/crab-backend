from django.db import models

from utils.models import CrabInfoModel


class Categoria(CrabInfoModel):

    categoria = models.CharField(
        verbose_name = "Categoria",
        max_length = 40,
        help_text = "Nombre de la categoria a la que pertenece una noticia"
    )

    def __str__(self):
        return self.categoria
