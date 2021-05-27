from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse


class Cretificates(TestCase):
    def setUp(self):
        self.client = APIClient()
        CERTIFICATE_URL = reverse("certificate:certificate-detail", args=[1])

    def retrive_certificate_by_user_permission(self):
        res = self.client.get(self.CERTIFICATE_URL, {"is_forstaff": "1"})
        # self.assertInHTML('')
