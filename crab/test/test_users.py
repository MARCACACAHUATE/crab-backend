import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTests(APITestCase):

    def setUp(self):
        self.url = "/users/"
        self.admin = User.objects.create_user(username="SuperAdmin", password="root123", email="admin@gmail.com", is_staff=True, is_verified=True)
        self.user = User.objects.create_user(username="userdummy", password="user123", email="user@gmail.com", is_verified=True)
        self.admin_credential = self.client.post("/users/login/", {"username": "SuperAdmin", "password": "root123"}).data["access"]
        self.user_credential = self.client.post("/users/login/", {"username": "userdummy", "password": "user123"}).data["access"]

    def test_create_new_user(self):
        """ Test para crear un usuario nuevo con los datos minimos necesarios."""
        data = {
            "username": "DonMafufada",
            "password": "PuroPincheCartelDeSanta19",
            "password_confirm": "PuroPincheCartelDeSanta19",
            "email": "ppcds@gmail.com",
            }
        response = self.client.post(self.url, data)
        queryset = User.objects.all()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(User.objects.get(username=data["username"]), queryset)

    def test_deactivate_user_by_admin(self):
        """ Test para desactivar un usuario utilizando un user admin."""
        self.client.credentials(HTTP_AUTHORIZATION= f"Bearer {self.admin_credential}")
        url = f"/users/{self.user.pk}/status/"
        data = { "is_active": False }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(False, response.data["is_active"])

    def test_deactivate_user_by_not_admin(self):
        """ Test para desactivar un usuario utilizando un user no admin."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_credential}")
        url = f"/users/{self.user.pk}/status/"
        data = { "is_active": True }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_users_not_admin(self):
        """ Test endpoint list user utilizando un user no admin. """
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_credential}")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_users_admin(self):
        """ Test endpoint list user utilizando un user admin. """
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_credential}")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
