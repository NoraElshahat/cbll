from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import MainAttendanceView, AttendanceUserPerVisitView, SignturesView

router = DefaultRouter()

router.register("main", MainAttendanceView)
router.register("visit/sign", AttendanceUserPerVisitView, basename="approved-users")
router.register("visit/signtures", SignturesView)

urlpatterns = [path("", include(router.urls))]
