from django.contrib import admin

from .models import Invoice


class AdminInvoice(admin.ModelAdmin):
    list_display = (
        "number_invoice",
        "name_coin",
        "vs_currency",
        "current_price",
        "amount",
        "total",
        "created",
    )


admin.site.register(Invoice, AdminInvoice)
