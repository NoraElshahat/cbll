from django.apps import AppConfig


class VisitConfig(AppConfig):
    name = "visit"

    def ready(self):
        import visit.signals

        return super().ready()
