from django.db import models
from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)
from django.dispatch import receiver

from invoice.views import create_invoice, create_invoice_failed
from contact.views import create_contact, create_contact_failed


class Logging(models.Model):
    user = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    result = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.user


@receiver(create_invoice)
def create_invoice_callback(sender, request, **kwargs):
    Logging.objects.create(
        action=f'Создание счета № {request.POST.get("number_invoice")}',
        result="Success",
        user=request.user.username,
    )


@receiver(create_invoice_failed)
def create_invoice_failed_callback(sender, request, **kwargs):
    Logging.objects.create(
        action=f'Создание счета № {request.POST.get("number_invoice")}',
        result="Failed",
        user=request.user.username,
    )


@receiver(create_contact)
def create_contact_callback(sender, request, **kwargs):
    Logging.objects.create(
        action="Отправка формы сообщения",
        result="Success",
        user=request.user.username if request.user.username else request.user,
    )


@receiver(create_contact_failed)
def create_contact_failed_callback(sender, request, **kwargs):
    Logging.objects.create(
        action="Отправка формы сообщения",
        result="Failed",
        user=request.user.username if request.user.username else request.user,
    )


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    Logging.objects.create(
        action="User logged in", result="Success", user=user.username
    )


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    Logging.objects.create(
        action="User logged out", result="Success", user=user.username
    )


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    Logging.objects.create(
        action="User login failed",
        result="Failed",
        user=credentials.get("username", None),
    )
