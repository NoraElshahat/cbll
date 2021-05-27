from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AnswersHandler,
    ComplexHanlder,
    ReportsView,
    ReportDownloader,
    QuestionHandler,
    NeedleHandler,
    QuestionType,
)


router = DefaultRouter()

router.register("main", ReportsView)
router.register("downloader", ReportDownloader)
router.register("questions", QuestionHandler, basename="questions")
router.register("needle", NeedleHandler, basename="needle")
router.register("question_types", QuestionType, basename="question_type")
router.register("answers", AnswersHandler, basename="answer")
router.register("complex", ComplexHanlder, basename="complex")


urlpatterns = [path("", include(router.urls))]
