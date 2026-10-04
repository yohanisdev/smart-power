from django.urls import path

from analytics.views import analytics_view

urlpatterns = [
    path('', analytics_view, name='analytics_page'),
]
