from django import urls
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CertificateDownloaderView

router = DefaultRouter()

router.register("user/print", CertificateDownloaderView)

urlpatterns = [path("", include(router.urls))]
