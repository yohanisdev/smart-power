from django.urls import path

from electricity.views import reading_create_view, reading_delete_view, reading_list_view, reading_update_view

urlpatterns = [
    path('', reading_list_view, name='reading_list'),
    path('new/', reading_create_view, name='reading_create'),
    path('<int:pk>/edit/', reading_update_view, name='reading_update'),
    path('<int:pk>/delete/', reading_delete_view, name='reading_delete'),
    path('import/', reading_create_view, name='reading_import'),
]
