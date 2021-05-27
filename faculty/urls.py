from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MainFacultyView


router = DefaultRouter()
router.register("main", MainFacultyView)

urlpatterns = [path("", include(router.urls))]
