from course.models import Course
from department.models import Department
from django.contrib.auth import get_user_model
from faculty.models import Faculty
from visit.models import Visit, VisitSites
from datetime import datetime
from equipment.models import Equipment
from report.models import Question, QuestionType, Needle

department_payload = {"name": "department-1"}

faculty_payload = {"name": "Faculty-1"}

visit_payload = {"name": "Visit-1", "objectives": "Visit-1Visit-1Visit-1Visit-1"}


visit_course = {"title": "titleasasd"}


def cerate_faculty():
    return Faculty.objects.create(**faculty_payload)


def cerate_department():
    department_payload.update({"faculty": cerate_faculty()})

    return Department.objects.create(**department_payload)


def create_equipment(faculty):
    return Equipment.objects.create(name="Equipment", faculty=faculty)


def cerate_visit(leader, faculty=None):
    visit_payload.update(
        leader=leader,
        site=create_site(),
        visit_course=create_visit_course(),
        department=cerate_department(),
    )

    if faculty:
        equipment = create_equipment(faculty=faculty)
        visit_payload.update(equipment=equipment)

    return Visit.objects.create(**visit_payload)


def create_leader(user_payload, params=None):
    if params:
        user_payload.update(params)

    return settings.AUTH_USER_MODEL.objects.create_staff_only(**user_payload)


def create_site():
    return VisitSites.objects.create(name="site-1", location="location")


def create_visit_course():
    return Course.objects.create(**visit_course)


def create_user(user_payload, params=None):
    if params:
        user_payload.update(params)

    return settings.AUTH_USER_MODEL.objects.create_user(**user_payload)


def create_question():
    payload = {"title": "A new question add", "question_type": create_type()}

    return Question.objects.create(**payload)


def create_type():
    return QuestionType.objects.create(title="menu")


def create_needle():

    return Needle.objects.create(init_value="1", question_type=1)
