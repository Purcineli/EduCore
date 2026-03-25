from django.apps import AppConfig


class AcademicoConfig(AppConfig):
    name = 'academico'

    def ready(self):
        import academico.signals  # noqa: F401
