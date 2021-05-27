from django.shortcuts import render
from rest_framework import viewsets, mixins, generics
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .models import Certificate
from .serializers import DetailedCeritificate
from rest_framework.authentication import TokenAuthentication


class CertificateDownloaderView(viewsets.GenericViewSet, mixins.RetrieveModelMixin):

    serializer_class = DetailedCeritificate
    queryset = Certificate.objects.all()

    # permission_classes = (IsAuthenticated, )
    # authentication_class = TokenAuthentication

    # def get_queryset(self):
    # return super().get_queryset()
    # request=self.request
    # return self.queryset.filter(users=request.user)
