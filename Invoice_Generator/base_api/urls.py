from django.urls import path
from .views import InvoiceGeneratorView

urlpatterns = [
    path('invoicegenerator/', InvoiceGeneratorView.as_view(), name='hello'),
]