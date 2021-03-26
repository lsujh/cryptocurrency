from django.views.generic.edit import CreateView
from django.contrib import messages
from django.dispatch import Signal

from .models import Contact


class ContactCreate(CreateView):
    model = Contact
    template_name = "contact/contact_new.html"
    fields = (
        "first_name",
        "last_name",
        "phone",
        "email",
        "message",
    )

    def get_initial(self):
        initial = super(ContactCreate, self).get_initial()
        if self.request.user.is_authenticated:
            initial["email"] = self.request.user.email
        return initial

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            create_contact.send(sender=self.__class__, request=request)
            messages.success(request, "Сообщение успешно отправлено")
            return self.form_valid(form)
        else:
            create_contact_failed.send(sender=self.__class__, request=request)
            messages.error(request, "Ошибка при отправке сообщения")
            return self.form_invalid(form)


create_contact = Signal(providing_args=["request"])
create_contact_failed = Signal(providing_args=["request"])
