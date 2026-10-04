from django.contrib.auth import get_user_model
from rest_framework import serializers

from appliances.models import Appliance
from billing.models import Tariff, TariffTier
from electricity.models import MeterReading
from homes.models import Home
from insights.models import Insight

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )


class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home
        fields = ('id', 'name', 'description', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class ApplianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appliance
        fields = (
            'id', 'home', 'name', 'category', 'power_watts', 'average_hours_per_day',
            'days_per_period', 'quantity', 'standby_power_watts', 'is_active',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class MeterReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeterReading
        fields = ('id', 'home', 'reading_value_kwh', 'reading_date', 'source', 'notes', 'created_at')
        read_only_fields = ('id', 'created_at')


class TariffTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = TariffTier
        fields = ('id', 'tariff', 'minimum_kwh', 'maximum_kwh', 'rate_per_kwh')
        read_only_fields = ('id',)


class TariffSerializer(serializers.ModelSerializer):
    tariff_tiers = TariffTierSerializer(many=True, read_only=True)

    class Meta:
        model = Tariff
        fields = ('id', 'name', 'provider', 'effective_from', 'effective_to', 'created_at', 'tariff_tiers')
        read_only_fields = ('id', 'created_at')


class InsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insight
        fields = ('id', 'home', 'type', 'title', 'message', 'severity', 'created_at')
        read_only_fields = ('id', 'created_at')
