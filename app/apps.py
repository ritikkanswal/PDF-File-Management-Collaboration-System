from django.apps import AppConfig
from django.contrib import admin



class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    def ready(self):
        # Import your models
        from .models import User, PDFFile, SharedFile, Comment

        # Register your models with the admin site
        admin.site.register(User)
        admin.site.register(PDFFile)
        admin.site.register(SharedFile)
        admin.site.register(Comment)





