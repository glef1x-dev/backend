from django.apps import AppConfig

from a12n import signals


class A12NConfig(AppConfig):
    name = "a12n"
    default = True

    def ready(self) -> None:
        from axes.signals import user_locked_out

        user_locked_out.connect(signals.raise_permission_denied)
