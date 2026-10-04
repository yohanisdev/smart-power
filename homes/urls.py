from django.urls import path

from homes.views import home_create_view, home_delete_view, home_detail_view, home_list_view, home_update_view

urlpatterns = [
    path('', home_list_view, name='home_list'),
    path('new/', home_create_view, name='home_create'),
    path('<int:pk>/', home_detail_view, name='home_detail'),
    path('<int:pk>/edit/', home_update_view, name='home_update'),
    path('<int:pk>/delete/', home_delete_view, name='home_delete'),
]
