from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.serializers import UsersSerializer
from visit.models import Visit

# from visit.serializers import  DetailVisitSerializer

from .models import ApprovedUserVisit, Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Attendance


class AttendanceUserPerVisitSerializer(serializers.ModelSerializer):
    visit = serializers.PrimaryKeyRelatedField(queryset=Visit.objects)
    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects)

    def validate(self, attrs):
        super().validate(attrs)

        if not "user" and "visit" in attrs.keys():
            raise ValueError("The required data in not sufficient", 404)

        return attrs

    class Meta:
        model = ApprovedUserVisit
        fields = ("user", "visit")


class AttendanceUserOnly(serializers.ModelSerializer):
    users = UsersSerializer(many=True)

    class Meta:
        fields = ("users",)
        model = Attendance


class DetailedAttendanceVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"


class SignturesSerilizers(serializers.ModelSerializer):
    parent_signture = serializers.FileField()

    class Meta:
        model = ApprovedUserVisit
        fields = ("id", "parent_signture")
