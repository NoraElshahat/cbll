from django.core.mail import EmailMessage, send_mail
from django.test import TestCase
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from rest_framework.test import APIClient

from visit.serializers import VisitPlanSerializer, VisitPlanDetailSerializer

from ._test_create_heplers import (
    cerate_department,
    cerate_faculty,
    cerate_visit,
    create_leader,
    create_user,
    create_visit_course,
    department_payload,
    faculty_payload,
    get_user_model,
    visit_course,
    visit_payload,
    create_equipment,
    create_type,
    create_question,
)

QUESTION_URL = reverse("questions-list")
QUESTION_TYPE_URL = reverse("question_type-list")
QUESTION_NEEDLE_URL = reverse("needle-list")
QUESTION_ANSWER_URL = reverse("answer-list")


class QuestionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.types = create_type()
        

    def test_create_answers_model(self):
        answers = []
        reses = []
        for letter in "ABCDEFG":
            for letter_inner in "ABCDEFG?":
                letter += letter_inner

            reses.append(
                self.client.post(
                    QUESTION_ANSWER_URL,
                    {"question": create_question().id, "body": letter},
                )
            )

        self.assertEqual(len(reses), 7)
