from django.db import models


class Invoice(models.Model):
    number_invoice = models.CharField("Номер счета", unique=True, max_length=19)
    name_coin = models.CharField("Монета", max_length=100)
    vs_currency = models.CharField("Валюта", max_length=50)
    current_price = models.FloatField("Цена")
    amount = models.IntegerField("Количество", default=1)
    total = models.FloatField("Сумма")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-number_invoice",)

    def __str__(self):
        return self.name_coin
