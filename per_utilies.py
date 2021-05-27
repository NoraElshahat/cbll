import csv

from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.utils import timezone
from datetime import datetime


def _prepare_csv_file(queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="test.csv"'
    writer = csv.writer(response)
    data = []
    data.append(["Question", "Activated", "Reort date", "user", "trip"])
    data.append(
        [
            queryset.first().question,
            "Yes",
            str(queryset.first().created_at),
            str(queryset.first().user),
            str(queryset.first().visit),
        ]
    )
    writer.writerows(data)

    return response


def _prepare_pdf_file(queryset, context=None):
    if not context:
        data = queryset.all()

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="test.pdf"'

    time = datetime.strftime(timezone.now(), "%Y-%m-%d")

    context = {"data": data, "time": time}

    html = render_to_string(template_name="report/report.html", context=context)
    pdf = pisa.CreatePDF(html, dest=response)

    return response
