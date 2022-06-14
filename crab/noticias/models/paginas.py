from django.db import models
from django.core.validators import URLValidator


class Pagina(models.Model):
    nombre_pagina = models.CharField(
        verbose_name = "Nombre de la pagina",
        max_length = 40,
        help_text = "Campo que almacena el nombre de la pagina"
    )
    url = models.CharField(
        verbose_name = "Url de la pagina",
        max_length = 100,
        help_text = "Campo que almacen el url de la pagina de las noticias",
        validators = [URLValidator,]
    )

    def __str__(self):
        return self.nombre_pagina