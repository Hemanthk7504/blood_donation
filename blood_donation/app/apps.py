from django.apps import AppConfig


class GraphQLAuthConfig(AppConfig):
    name = "app"
    verbose_name = "Blood app"

    def ready(self):
        import app.signals