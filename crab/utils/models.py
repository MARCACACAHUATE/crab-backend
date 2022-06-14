from django.db import models


class CrabInfoModel(models.Model):
    """ Modelo Base para todos los otros models
        Este modelo abstracto provee los campos:
        + created (DateTime)
        + modified (DateTime)
    """

    created = models.DateTimeField(
        verbose_name = "Creado en",
        auto_now_add = True,
        help_text = "Campo DateTime en el cual el usuario fue creado"
    )
    modified = models.DateTimeField(
        verbose_name = "Modificado en",
        auto_now = True,
        help_text = "Campo DateTime en el cual el usuario fue modificado"
    )

    class Meta:
        abstract = True
        get_latest_by = "created"
        ordering = ["-created", "-modified"]