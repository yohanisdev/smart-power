from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from analytics.services import actual_household_usage, appliance_breakdown, daily_usage, estimate_appliance_usage
from api.serializers import ApplianceSerializer, HomeSerializer, InsightSerializer, MeterReadingSerializer, UserRegistrationSerializer
from appliances.models import Appliance
from electricity.models import MeterReading
from homes.models import Home
from insights.models import Insight


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response({'detail': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'detail': 'Login successful.'})
        return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'detail': 'Logged out.'})


class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'username': request.user.username, 'email': request.user.email})


class HomeViewSet(viewsets.ModelViewSet):
    serializer_class = HomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Home.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ApplianceViewSet(viewsets.ModelViewSet):
    serializer_class = ApplianceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Appliance.objects.filter(home__user=self.request.user)


class MeterReadingViewSet(viewsets.ModelViewSet):
    serializer_class = MeterReadingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MeterReading.objects.filter(home__user=self.request.user)


class InsightViewSet(viewsets.ModelViewSet):
    serializer_class = InsightSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Insight.objects.filter(home__user=self.request.user)


class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        home = request.user.homes.first()
        if not home:
            return Response({'actual_usage': 0, 'estimated_usage': 0, 'breakdown': []})
        summary = {
            'home_id': home.id,
            'home_name': home.name,
            'actual_usage': float(actual_household_usage(home)),
            'estimated_usage': float(estimate_appliance_usage(home)),
            'breakdown': appliance_breakdown(home),
            'daily': daily_usage(home),
        }
        return Response(summary)


class DailyAnalyticsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        home = request.user.homes.first()
        if not home:
            return Response({'data': []})
        return Response({'data': daily_usage(home)})


class WeeklyAnalyticsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'data': []})


class MonthlyAnalyticsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'data': []})


def actual_vs_estimated(request):
    if not request.user.is_authenticated:
        return Response({'detail': 'Authentication required.'}, status=401)
    home = request.user.homes.first()
    if not home:
        return Response({'actual_usage': 0, 'estimated_usage': 0})
    return Response({
        'actual_usage': float(actual_household_usage(home)),
        'estimated_usage': float(estimate_appliance_usage(home)),
    })
