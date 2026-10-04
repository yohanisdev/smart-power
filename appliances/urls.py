from django.urls import path

from appliances.views import appliance_create_view, appliance_delete_view, appliance_list_view, appliance_update_view

urlpatterns = [
    path('', appliance_list_view, name='appliance_list'),
    path('new/', appliance_create_view, name='appliance_create'),
    path('<int:pk>/edit/', appliance_update_view, name='appliance_update'),
    path('<int:pk>/delete/', appliance_delete_view, name='appliance_delete'),
]
