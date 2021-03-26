from django.urls import path
from . import views

app_name = "invoice"

urlpatterns = [
    path("", views.ListCoinView.as_view(), name="list_coin"),
    path(
        "create/<str:coin>/<str:currency>/",
        views.CreateInvoice.as_view(),
        name="create_invoice",
    ),
]
