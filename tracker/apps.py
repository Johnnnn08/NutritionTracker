from django.apps import AppConfig

class TrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracker'

    # 👇 Add this method to import your signals
    def ready(self):
        import tracker.signals