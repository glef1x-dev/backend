from app.base_config import AppConfig


class BlogConfig(AppConfig):
    name = "blog"
    default = True

    def ready(self) -> None:
        import blog.signals  # noqa
