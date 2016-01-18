from django.apps import AppConfig


class TheappConfig(AppConfig):
    name = 'theapp'

    def ready(self):
        from theapp import signals
