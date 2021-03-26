import requests

from django.urls import reverse_lazy
from django.dispatch import Signal
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Invoice
from .list_coin import list_coin
from .list_currency import list_currency
from .forms import CurencyForm, CreateInvoiceForm


class ListCoinView(ListView):
    template_name = "invoice/list_coin.html"

    def get(self, request, *args, **kwargs):
        vs_currency = "usd"
        currency = request.GET.get("currency")
        if currency:
            request.session["currency"] = currency
            vs_currency = currency
        elif request.session.get("currency"):
            vs_currency = request.session.get("currency")
        form = CurencyForm(initial={"currency": vs_currency})
        if request.GET.get("page"):
            if not request.GET.get("page"):
                next_page = 2
                prev_page = 0
                page = 1
            elif int(request.GET.get("page")) > 0:
                next_page = int(request.GET.get("page")) + 1
                prev_page = int(request.GET.get("page")) - 1
                page = int(request.GET.get("page"))
        else:
            next_page = 2
            prev_page = 0
            page = 1
        url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={vs_currency}&order=market_cap_desc&per_page=100&page={page}&sparkline=false"
        results = requests.get(url).json()
        self.object_list = results
        context = {
            "form": form,
            "results": results,
            "vs_currency": vs_currency,
            "next_page": str(next_page),
            "prev_page": str(prev_page),
            "page": str(page),
        }
        return self.render_to_response(context)


class CreateInvoice(LoginRequiredMixin, CreateView):
    template_name = "invoice/create_invoice.html"
    model = Invoice
    form_class = CreateInvoiceForm
    success_url = reverse_lazy("invoice:list_coin")

    def get_initial(self):
        initial = super(CreateInvoice, self).get_initial()
        number_invoice = Invoice.objects.all().first()
        if number_invoice:
            number = str(int("".join(number_invoice.number_invoice.split(" "))) + 1)
        else:
            number = "1000000000000000"
        coin = self.kwargs.get("coin")
        currency = self.kwargs.get("currency")
        coin_id = [i["id"] for i in list_coin if i["name"] == coin][0]
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={currency}"
        result = requests.get(url).json()
        initial["number_invoice"] = " ".join(
            [number[i : i + 4] for i in range(0, 16, 4)]
        )
        initial["name_coin"] = coin
        initial["vs_currency"] = [i[1] for i in list_currency if i[0] == currency][0]
        initial["current_price"] = result[coin_id][currency]
        return initial

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            current_price = float(form.data.get("current_price"))
            amount = int(form.data.get("amount"))
            coin = form.data.get("name_coin")
            currency = form.data.get("vs_currency")
            form.instance.total = current_price * amount
            create_invoice.send(sender=self.__class__, request=request)
            messages.success(
                request,
                f'Счет № {form.data.get("number_invoice")} успешно создан. '
                f"Монета - {coin}. Валюта - {currency} {current_price}. Количество - {amount} "
                f"Сумма - {form.instance.total}",
            )
            return self.form_valid(form)
        else:
            create_invoice_failed.send(sender=self.__class__, request=request)
            messages.error(request, "Ошибка создания счета")
            return self.form_invalid(form)


create_invoice = Signal(providing_args=["request"])
create_invoice_failed = Signal(providing_args=["request"])
