from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/dashboard/', permanent=False), name='index'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('homes/', include('homes.urls')),
    path('appliances/', include('appliances.urls')),
    path('readings/', include('electricity.urls')),
    path('billing/', include('billing.urls')),
    path('analytics/', include('analytics.urls')),
    path('insights/', include('insights.urls')),
    path('api/', include('api.urls')),
    path('dashboard/', include('analytics.dashboard_urls')),
]
