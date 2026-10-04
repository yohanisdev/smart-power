from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views import (
    ApplianceViewSet,
    DashboardAPIView,
    DailyAnalyticsAPIView,
    HomeViewSet,
    InsightViewSet,
    LoginAPIView,
    LogoutAPIView,
    MeAPIView,
    MeterReadingViewSet,
    MonthlyAnalyticsAPIView,
    RegisterAPIView,
    WeeklyAnalyticsAPIView,
    actual_vs_estimated,
)

router = DefaultRouter()
router.register(r'homes', HomeViewSet, basename='homes')
router.register(r'appliances', ApplianceViewSet, basename='appliances')
router.register(r'readings', MeterReadingViewSet, basename='readings')
router.register(r'insights', InsightViewSet, basename='insights')

urlpatterns = [
    path('auth/register/', RegisterAPIView.as_view(), name='api-register'),
    path('auth/login/', LoginAPIView.as_view(), name='api-login'),
    path('auth/logout/', LogoutAPIView.as_view(), name='api-logout'),
    path('auth/me/', MeAPIView.as_view(), name='api-me'),
    path('analytics/daily/', DailyAnalyticsAPIView.as_view(), name='api-analytics-daily'),
    path('analytics/weekly/', WeeklyAnalyticsAPIView.as_view(), name='api-analytics-weekly'),
    path('analytics/monthly/', MonthlyAnalyticsAPIView.as_view(), name='api-analytics-monthly'),
    path('analytics/actual-vs-estimated/', actual_vs_estimated, name='api-actual-vs-estimated'),
    path('dashboard/', DashboardAPIView.as_view(), name='api-dashboard'),
] + router.urls
