from rest_framework import serializers
from users.serializers import UsersSerializer
from visit.serializers import DetailVisitSerializer
from .models import Certificate


class DetailedCeritificate(serializers.ModelSerializer):
    user = UsersSerializer()
    visit = DetailVisitSerializer()

    class Meta:
        model = Certificate
        fields = "__all__"
