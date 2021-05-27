from django.contrib.auth import authenticate, get_user_model
from django.http import HttpResponse
from rest_framework import generics, mixins, permissions, views, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser as IsStaff
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from .permissions import IsSuperAdminUser
from .serializers import (
    StudenSerializer,
    StudentLoginSerializer,
    SuperAdminSerializer,
    SupervisorSerializer,
    UserSerializer,
    RemoveVisitUserSerializer
)


class StudentView(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, AllowAny)

    serializer_class = StudenSerializer
    queryset = get_user_model().objects.filter(
        is_staff=False, is_super_admin=False, is_superuser=False
    )


class UserSerializerView(viewsets.GenericViewSet, mixins.ListModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = get_user_model().objects
    serializer_class = UserSerializer

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(id=Token.objects.get(key=self.request.auth).user.id)
        )


class SupervisorView(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsStaff)

    serializer_class = SupervisorSerializer
    queryset = get_user_model().objects.filter(
        is_staff=True, is_super_admin=False, is_superuser=False
    )


class StudentLogin(ObtainAuthToken):
    permission_classes = (AllowAny,)
    serializer_class = StudentLoginSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserLogout(views.APIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        get_object_or_404(get_user_model(), pk=request.user.id)
        logout(request)

        if request.user.is_authenticated:
            raise ValueError('something went wrong')

        return Response({'logout': True})

class SuperAdminView(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperAdminUser)

    serializer_class = SuperAdminSerializer
    queryset = get_user_model().objects.filter(is_super_admin=True)


class RemoveVisitUser(
    viewsets.GenericViewSet,
    mixins.UpdateModelMixin
    ):
    queryset = get_user_model().objects
    serializer_class = RemoveVisitUserSerializer
