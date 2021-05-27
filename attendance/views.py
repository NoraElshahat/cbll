from django.shortcuts import render
from rest_framework import generics, mixins, views, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from users.permissions import IsSuperAdminUser

from .models import ApprovedUserVisit, Attendance
from .serializers import (
    AttendanceSerializer,
    AttendanceUserPerVisitSerializer,
    DetailedAttendanceVisitSerializer,
    SignturesSerilizers,
)


class MainAttendanceView(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):

    # permission_classes = (IsAuthenticated, )
    # authentication_classes = (TokenAuthentication, )
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DetailedAttendanceVisitSerializer

        return self.serializer_class


class AttendanceUserPerVisitView(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
):

    queryset = ApprovedUserVisit.objects.all()
    serializer_class = AttendanceUserPerVisitSerializer
    # authentication_classes = (TokenAuthentication, )
    # permission_classes = (IsAuthenticated, IsSuperAdminUser)


class SignturesView(
    viewsets.GenericViewSet,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    queryset = ApprovedUserVisit.objects.all()

    serializer_class = SignturesSerilizers
