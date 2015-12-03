from django.apps import AppConfig


class BareConfig(AppConfig):
    name = 'bare'

    def ready(self):

        # import signal handlers
        import bare.signals
