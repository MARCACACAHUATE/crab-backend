from django.db import models


class Noticia(models.Model):
    titulo = models.CharField(
        verbose_name = "Titulo de la noticia",
        max_length = 40,
        help_text = "Este campo muestra el titulo de la noticia, el cual es obligatorio"
    )
    contenido = models.TextField(
        verbose_name = "Contenido de la noticia",
        help_text = "Este campo muestra todo el contenido de una noticia"
    )
    fecha = models.DateTimeField(
        verbose_name = "Fecha de la noticia",
        help_text = "Este campo almacena el fecha en al que fue publicada la noticia"
    )
    categoria = models.ForeignKey(to="noticias.Categoria", on_delete=models.CASCADE)
    pagina = models.ForeignKey(to="noticias.Pagina", on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo