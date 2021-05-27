from rest_framework import serializers
from .models import Meeting


class MeetingsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id",)
        models = Meeting


class MeetingDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("title", "time", "location")
        model = Meeting
        depth = 2
