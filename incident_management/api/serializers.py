from rest_framework import serializers
from incident_management.models import (
    Market,
    Incident,
    IncidentStatus,
    IncidentUpdate,
    ITSMService,
    IncidentPriority,
    Service,
    SystemServices,
    EmailDistributionList)


class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = '__all__'


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = '__all__'
        read_only_fields = ['id']


class ITSMServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ITSMService
        fields = '__all__'

class IncidentPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentPriority
        fields = '__all__'


class IncidentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentUpdate
        fields = '__all__'


class SystemServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemServices
        fields = '__all__'


class IncidentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentStatus
        fields = '__all__'


class EmailDistributionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailDistributionList
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'




