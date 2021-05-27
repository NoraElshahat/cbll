from rest_framework import serializers
from .models import Faculty


class MainFacultySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Faculty
