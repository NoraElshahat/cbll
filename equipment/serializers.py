from rest_framework import serializers
from visit.serializers import DetailVisitSerializer
from .models import Equipment


class EquipmetsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Equipment


class DetailedEquipmentSerializer(EquipmetsSerializer):
    visit = DetailVisitSerializer(many=True)
