from django.contrib import admin
from .models import Report, Question, QuestionType, Needle, Answer, ComplexReport


class ReportAdmin(admin.ModelAdmin):
    list_display = ["title", "is_active", "is_for_staff", "to_beactive_in"]


admin.site.register(Report, ReportAdmin)
admin.site.register(Question)
admin.site.register(QuestionType)
admin.site.register(Answer)
admin.site.register(Needle)
admin.site.register(ComplexReport)
