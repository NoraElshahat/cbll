from rest_framework import serializers
from .models import Report, Question, Needle, QuestionType, Answer
from users.serializers import UsersSerializer
from visit.serializers import DetailVisitSerializer


class ListReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ("id",)


class DetailedReportSerializer(serializers.ModelSerializer):
    user = UsersSerializer()
    visit = DetailVisitSerializer()

    class Meta:
        model = Report
        fields = "__all__"


class ReportDownloaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"


class NeedlesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Needle


class NeedleSerializer(NeedlesSerializer):
    class Meta:
        fields = "__all__"
        model = Needle
        depth = 3


class QuestionTypesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = QuestionType


class QuestionTypeSerializer(QuestionTypesSerializer):
    class Meta:
        fields = ("id", "title", "question_set")
        model = QuestionType
        depth = 2


class EmbededNeedleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "init_value")
        model = Needle


class ComplexVisitReport(serializers.ModelSerializer):
    # questions = QuestionSerializer(many=True)
    visit = DetailVisitSerializer()

    class Meta:
        fields = ("id", "visit", "questions")
        model = Report


class AnswersSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"
        # fields = ('__all__')


class AnswerSerialzier(AnswersSerialzier):
    class Meta:
        model = Answer
        fields = "__all__"


class EmbeddedAnswerSerializer(AnswerSerialzier):
    class Meta:
        model = Answer
        fields = ("id", "body", "file_to")


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "title")
        model = Question


class QuestionSerializer(QuestionsSerializer):
    proposed_values = EmbededNeedleSerializer(many=True, source="needle_set_active")

    proposed_values_no = serializers.IntegerField(source="needle_set_no")
    answer_set = EmbeddedAnswerSerializer(many=True)

    class Meta:
        fields = (
            "id",
            "title",
            "question_type",
            "proposed_values",
            "answer_set",
            "proposed_values_no",
        )
        model = Question
        depth = 2
