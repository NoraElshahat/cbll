from attendance.models import ApprovedUserVisit
from django.core.mail import send_mail
from rest_framework import generics, mixins, views, viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

from django.urls import reverse
from django.shortcuts import get_list_or_404 
from visit.signals import (
    visit_applied_students_mail,
    visit_applied_leader_mail,
    visit_applied_deans_mail
    )


from django.contrib.auth import get_user_model
from users.models import BlockedStudents
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from users.permissions import IsSuperAdminUser
from django.db.utils import IntegrityError

from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework.status import HTTP_204_NO_CONTENT

from django.shortcuts import get_object_or_404
import json
from .models import Visit, VisitSites, Activity
from .serializers import (
    DetailedVisitReportSerializer,
    DetailVisitSerializer,
    MainVisitSerializer,
    ListVisitReportSerializer,
    UploadPhotoSerializer,
    DetailedActivitiesSerializer,
    ListActivitiesSerializer,
    VisitStudentsSerilaizer,
    VisitPlanSerializer,
    VisitPlanDetailSerializer,
    RemoveVisitUserSerializer
)

# visits of current_user.department
class InitVisit(viewsets.GenericViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Visit.objects.all()

    def get_queryset(self):
        self.queryset=self.queryset.filter(department=self.request.user.department)

        code = self.request.query_params.get("code")
        if code:
            return self.queryset.filter(code=code)

        return self.queryset


class MainVisitView(
    InitVisit,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):

    def _add_student_by_token(self):
        user = self.request.user
        visit = self.get_object()
        visit.students.add(user)

    serializer_class = MainVisitSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DetailVisitSerializer
        return self.serializer_class
    
    def partial_update(self, request, *args, **kwargs):
        visit = self.get_object()
        # student = Token.objects.get(key=self.request.auth).user
       
        visit_applied_deans_mail.send(
            visit   = visit,
            deans   = get_list_or_404(get_user_model(), is_staff=True, is_superuser=True),
            student = request.user,
            sender  = Visit,
            request = request
        )

        visit_applied_leader_mail.send(
            visit = visit,
            leader=visit.leader,
            student = request.user,
            token=Token.objects.get(user=request.user),
            sender=Visit,
            request = request,
            remove_user_url=request.build_absolute_uri(reverse('visit:remove-visit-user-detail'))
        )

        visit_applied_students_mail.send(
            visit = visit,
            student = request.user,
            sender=Visit,
            request= request
            )
        
        self._add_student_by_token()

        return super().partial_update(request, *args, **kwargs)

class RemoveVisitUser(views.APIView):
    authentication_classes  = (SessionAuthentication, )
    queryset = Visit.objects.all()

    def post(self, request):
        data = request.data
        visit = get_object_or_404(self.queryset, pk= data.get('visit'))
        student = Token.objects.get(key=request.data.get('student')).user

        if bool(int(data.get('remove', False))):
            visit.students.remove(student)
            BlockedStudents.objects.create(visit=visit, student=student, reason=data.get('reason', 'removed by admin'))
            
            if not visit.students.filter(id=student.id).exists():
                return Response({'student_removed': True}, 200)
        
        visit.students.add(student)

        blocked_stundet = BlockedStudents.objects.filter(visit=visit, student=student)
        blocked_stundet.delete() if blocked_stundet.exists() else ''
            
        if not visit.students.filter(id=student.id).exists():
            raise ValueError('something went wrong')

        return Response({'student_added': True}, 200)

class ReportsVisitView(
    InitVisit,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    serializer_class = ListVisitReportSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DetailedVisitReportSerializer
        return self.serializer_class


class UploadPhotoView(
    InitVisit, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin
):

    serializer_class = UploadPhotoSerializer


class ListActivitiesView(
    InitVisit, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin
):
    queryset = Activity.objects.all()

    serializer_class = ListActivitiesSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return self.serializer_class

        return DetailedActivitiesSerializer


class VisitPlan(
    InitVisit, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin
):

    serializer_class = VisitPlanSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return VisitPlanDetailSerializer

        return self.serializer_class

# class FindVisit(InitVisit)