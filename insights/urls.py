from django.urls import path

from insights.views import insight_list_view

urlpatterns = [
    path('', insight_list_view, name='insight_list'),
]
