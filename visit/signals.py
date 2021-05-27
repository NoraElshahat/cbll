from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime, timedelta
from visit.models import Visit, DATE_FORMAT
from django.core.signals import (
    request_started,
    request_finished
    )

from typing import List, Dict
from faculty.models import Faculty
from report.models import Report
from django.dispatch import receiver, Signal
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.template import RequestContext
visit_applied_students_mail = Signal()
visit_applied_leader_mail = Signal()
visit_applied_deans_mail = Signal()


BASE_VISITS_URL = 'mails/visits/applied/'
'''

{
   "students": [2]
}

'''

def _prepare_email(template_path: str, kwargs: Dict, to_: List):
    template = render_to_string(
        f'{BASE_VISITS_URL}{template_path}/main.html',
        request=kwargs.pop('request'),
        context= kwargs,
    )

    mail = EmailMessage(
    subject=str(kwargs.get('visit')),
    body=template,
    from_email='cbl.advisor@hu.edu.eg',
    to=to_
    )

    mail.content_subtype = 'html'
    mail.send()

@receiver(visit_applied_students_mail, sender=Visit)
def send_student_mail(sender, **kwargs):
    _prepare_email(
        'student',
        kwargs,
        ['abdallah.attallah@sekem.org']
        )

@receiver(visit_applied_leader_mail, sender=Visit)
def visit_applied_leader_send_mail(sender, **kwargs):
    _prepare_email(
        'leader',
        kwargs,
        ['abdallah.attallah@sekem.org']
        )

@receiver(visit_applied_deans_mail, sender=Visit )
def visit_applied_deans_send_mail(sender, **kwargs):
      _prepare_email(
        'student',
        kwargs,
        [kwargs['student']]
        )
