from django.contrib import admin

from .models import Logging


class AdminLogging(admin.ModelAdmin):
    list_display = (
        "user",
        "action",
        "result",
        "created",
    )


admin.site.register(Logging, AdminLogging)
