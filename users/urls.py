from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from users.views import (
    StudentLogin,
    StudentView,
    SupervisorView,
    SuperAdminView,
    RemoveVisitUser,
    UserSerializerView,
    UserLogout
)

router = DefaultRouter()
router.register("students", StudentView, basename="students")
router.register("remove-visit", RemoveVisitUser, basename="visit-remove-user")
router.register("supervisors", SupervisorView, basename="supervisors")
router.register("superadmins", SuperAdminView, basename="superadmins")
router.register("serialize", UserSerializerView, basename="user-serializer"),

app_name = "users"

urlpatterns = [
    path("", include(router.urls)), path("login/", StudentLogin.as_view()),
    path("logout/", UserLogout.as_view(), name='logout')
    ]

