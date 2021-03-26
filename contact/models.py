from django.db import models


class Contact(models.Model):
    email = models.EmailField("Email")
    first_name = models.CharField("Имя", max_length=50)
    last_name = models.CharField("Фамилия", max_length=50)
    phone = models.CharField("Телефон", max_length=15)
    message = models.TextField("Сообщение")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.email
