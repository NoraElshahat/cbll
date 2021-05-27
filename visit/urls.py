from django.urls import path, include, reverse
from .views import (
    MainVisitView,
    ReportsVisitView,
    UploadPhotoView,
    ListActivitiesView,
    RemoveVisitUser,
    VisitPlan,
)
from rest_framework.routers import DefaultRouter

app_lable = "visit"

app_name = "visit"

router = DefaultRouter()

router.register("main",         MainVisitView,      basename="visit")
router.register("plans",        VisitPlan,          basename="visit-plan")
router.register("reports",      ReportsVisitView,   basename="visit-reports")
router.register("activities",   ListActivitiesView, basename="activities")
router.register("photo/upload", UploadPhotoView,    basename="visit-photos")
# router.register("find-visit", FindVisit,    basename="find-visit")

urlpatterns = [
    path("", include(router.urls)),
    path('remove-user/', RemoveVisitUser.as_view(), name='remove-visit-user-detail')
]