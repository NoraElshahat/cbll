from rest_framework import viewsets, mixins, generics
from .models import Faculty
from .serializers import MainFacultySerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class MainFacultyView(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin
):

    serializer_class = MainFacultySerializer
    queryset = Faculty.objects.all()
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,  )
