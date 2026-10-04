from django.urls import path

from billing.views import billing_overview

urlpatterns = [
    path('', billing_overview, name='billing_overview'),
]
