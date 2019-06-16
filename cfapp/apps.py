from django.apps import AppConfig


class CfappConfig(AppConfig):
    name = 'cfapp'
    verbose_name = 'crows flock'

    def ready(self):
        import cfapp.signals  # pylint: disable=W0611
