from datetime import date

from rest_framework import status
from rest_framework.test import APITestCase
from faker import Faker

from users.models import User
from noticias.models import Categoria, Pagina, Noticia


faker = Faker()

class NoticiasTestCase(APITestCase):

    def setUp(self):
        self.pagina = Pagina.objects.create(nombre_pagina="pagina prueba", url="prueba.com")
        self.categoria = Categoria.objects.create(categoria="categoria1")
        self.user = User.objects.create_user(
                username="noticias_creator",
                password="noticias123",
                email="noticias@gmail.com",
                is_verified=True,
                is_staff=True
                )
        self.admin_credential = self.client.post("/users/login/", {"username": "noticias_creator", "password": "noticias123"}).data["access"]
        # esta parte es temporal
        Noticia.objects.create(titulo=faker.text(max_nb_chars=10), contenido=faker.paragraph(nb_sentences=1), fecha=faker.date_this_decade().isoformat(), categoria=self.categoria, pagina=self.pagina)

    def test_crear_noticias(self):
        """ Test para registar noticias en la base de datos"""
        url = "/noticias/"
        noticias = [{"titulo": faker.text(max_nb_chars=10), "contenido": faker.paragraph(nb_sentences=1), "fecha": faker.date_this_decade(), "categoria": 1} for _ in range(10)]
        data = {
            "pagina": "pagina prueba",
            "noticias": noticias
                }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(noticias), response.data["data"]["total_noticias"])

    def test_delete_noticia_by_admin(self):
        """ Test para eliminar una noticia."""
        id = Noticia.objects.first().id
        url = f"/noticias/{id}/"
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_credential}")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_list_noticias(self):
        """ Test para listar las noticias utilizando fechas."""
        fecha = date(2021, 1, 12).isoformat()
        fecha_fin = date(2022, 1, 31).isoformat()

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_credential}")
        url = f"/noticias/?fecha={fecha}&fecha_fin={fecha_fin}"
        respnse = self.client.get(url)
        self.assertEqual(respnse.status_code, status.HTTP_200_OK)
