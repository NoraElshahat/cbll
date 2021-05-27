from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import (
    QuestionsSerializer,
    QuestionSerializer,
    DetailedReportSerializer,
    ListReportSerializer,
    NeedlesSerializer,
    NeedleSerializer,
    ReportDownloaderSerializer,
    QuestionTypesSerializer,
    QuestionTypeSerializer,
    ComplexVisitReport,
    AnswersSerialzier,
    AnswerSerialzier,
)

from .models import Report, Question, Needle, QuestionType, Answer
from per_utilies import _prepare_csv_file, _prepare_pdf_file


class InitReport(viewsets.GenericViewSet):
    # authentication_classes = (TokenAuthentication, )
    # permission_classes     = (IsAuthenticated, )
    queryset = Report.objects.all()


class ReportsView(InitReport, mixins.RetrieveModelMixin, mixins.ListModelMixin):

    serializer_class = ListReportSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DetailedReportSerializer

        return ListReportSerializer


class ReportDownloader(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Report.objects.all()

    def list(self, request):
        return _prepare_pdf_file(self.queryset)


class QuestionHandler(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionsSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return QuestionSerializer

        return self.serializer_class


class NeedleHandler(QuestionHandler):
    queryset = Needle.objects.all()
    serializer_class = NeedlesSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return NeedleSerializer

        return self.serializer_class


class QuestionType(NeedleHandler):
    queryset = QuestionType.objects.all()
    serializer_class = QuestionTypesSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return QuestionTypeSerializer

        return self.serializer_class


class ComplexHanlder(viewsets.ModelViewSet):
    serializer_class = ComplexVisitReport
    queryset = Report.objects.all()
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)


class AnswersHandler(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
):
    serializer_class = AnswersSerialzier
    queryset = Answer.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AnswerSerialzier
        return self.serializer_class
