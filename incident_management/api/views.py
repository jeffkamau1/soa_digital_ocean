from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, generics
from django.contrib.auth import authenticate
from django.shortcuts import render

from incident_management.api.serializers import (IncidentSerializer, MarketSerializer,
                                                 ITSMServiceSerializer, IncidentUpdateSerializer,
                                                 SystemServicesSerializer, IncidentPrioritySerializer,
                                                 IncidentStatusSerializer, ServiceSerializer,
                                                 EmailDistributionListSerializer)
from incident_management.api.permissions import IsIncidentManager
from incident_management.models import (Market, Service, ITSMService, Incident, SystemServices,
                                        IncidentStatus, IncidentUpdate, EmailDistributionList, IncidentPriority)
from drf_spectacular.utils import extend_schema
from utils.send_email_verification import send_verification_email

from django.http import HttpResponse


def health_check(request):
    return HttpResponse("Website is healthy")


class IncidentCreateView(generics.CreateAPIView):
    """Allows one to create an inicdent"""
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    permission_classes = [IsIncidentManager]

    def perform_create(self, serializer):
        # Assign the user making the request to the 'created_by' field
        serializer.save(created_by=self.request.user)


class IncidentUpdateView(generics.UpdateAPIView):
    """Allows one to update an incident"""
    serializer_class = IncidentSerializer
    permission_classes = [IsIncidentManager]

    @extend_schema(request=IncidentSerializer, responses=None)
    def get_queryset(self):
        queryset = Incident.objects.all()
        return queryset


class IncidentListView(generics.ListAPIView):
    """Lists all incidents"""
    serializer_class = IncidentSerializer

    @extend_schema(request=IncidentSerializer, responses=None)
    def get_queryset(self):
        queryset = Incident.objects.all()
        return queryset


class IncidentRetrieveView(generics.RetrieveAPIView):
    """Allows one to retrieve an incident"""
    serializer_class = IncidentSerializer

    @extend_schema(request=IncidentSerializer, responses=None)
    def get_queryset(self):
        queryset = Incident.objects.all()
        return queryset


class IncidentCommentUpdateListView(generics.ListAPIView):
    """Allows one to retrieve all incident updates of an inicdent"""
    serializer_class = IncidentUpdateSerializer
    permission_classes = [IsIncidentManager]

    @extend_schema(request=IncidentUpdateSerializer, responses=None)
    def get_queryset(self):
        incident_id = generics.get_object_or_404(Incident, incident_id=self.kwargs['incident_id'])
        return IncidentUpdate.objects.filter(incident_id=incident_id)


class IncidentCommentUpdateCreateView(generics.CreateAPIView):
    """Allows one to create an update of an incident"""
    serializer_class = IncidentUpdateSerializer
    permission_classes = [IsIncidentManager]

    @extend_schema(request=IncidentUpdateSerializer, responses=None)
    def perform_create(self, serializer):
        incident_update = generics.get_object_or_404(IncidentUpdate, incident_id=self.kwargs['incident_id'])
        serializer.save(incident_update=incident_update, updated_by=self.request.user)


class IncidentCommentRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """Allows one to retrieve and update an incident update """
    queryset = IncidentUpdate.objects.all()
    serializer_class = IncidentUpdateSerializer
    permission_classes = [IsIncidentManager]

    @extend_schema(request=IncidentUpdateSerializer, responses=None)
    def get_object(self):
        incident = generics.get_object_or_404(Incident, incident_id=self.kwargs['incident_id'])
        return generics.get_object_or_404(IncidentUpdate, pk=self.kwargs['pk'], incident=incident)


class ListMarkets(generics.ListAPIView):
    """Allows one to list all markets"""
    serializer_class = MarketSerializer

    @extend_schema(request=MarketSerializer, responses=None)
    def get_queryset(self):
        queryset = Market.objects.all()
        return queryset


class RetrieveMarkets(generics.RetrieveAPIView):
    """Allows one to retrive a single market"""
    serializer_class = MarketSerializer

    @extend_schema(request=MarketSerializer, responses=None)
    def get_queryset(self):
        queryset = Market.objects.all()
        return queryset


class IncidentPriorityListView(generics.ListAPIView):
    """Allows one to list incident priorities eg P1, P2"""
    serializer_class = IncidentPrioritySerializer

    @extend_schema(request=IncidentPrioritySerializer, responses=None)
    def get_queryset(self):
        queryset = IncidentPriority.objects.all()
        return queryset


class IncidentPriorityRetrieveView(generics.RetrieveAPIView):
    """Allows one to retrieve a single incident priority"""
    serializer_class = IncidentPrioritySerializer

    @extend_schema(request=IncidentPrioritySerializer, responses=None)
    def get_queryset(self):
        queryset = IncidentPriority.objects.all()
        return queryset


class SystemServicesListView(generics.ListAPIView):
    """Allows one to retrieve all system services"""
    serializer_class = SystemServicesSerializer

    @extend_schema(request=SystemServicesSerializer, responses=None)
    def get_queryset(self):
        queryset = SystemServices.objects.all()
        return queryset


class SystemServicesRetrieveView(generics.RetrieveAPIView):
    """Allows one to retrieve a systemservice"""
    serializer_class = SystemServicesSerializer

    @extend_schema(request=SystemServicesSerializer, responses=None)
    def get_queryset(self):
        queryset = SystemServices.objects.all()
        return queryset


class ServiceListView(generics.ListAPIView):
    """Allows one to get all services"""
    serializer_class = ServiceSerializer

    @extend_schema(request=ServiceSerializer, responses=None)
    def get_queryset(self):
        queryset = Service.objects.all()
        return queryset


class ServiceRetrieveView(generics.RetrieveAPIView):
    """Allows one to retrieve an incident"""
    serializer_class = ServiceSerializer

    @extend_schema(request=ServiceSerializer, responses=None)
    def get_queryset(self):
        queryset = Service.objects.all()
        return queryset


class ITSMServiceListView(generics.ListAPIView):

    """Allows one to retrieve all ITSM services"""
    serializer_class = ITSMServiceSerializer

    @extend_schema(request=ITSMServiceSerializer, responses=None)
    def get_queryset(self):
        queryset = ITSMService.objects.all()
        return queryset


class ITSMServiceRetrieveView(generics.RetrieveAPIView):
    """Allows one to retrieve a single ITSM service"""
    serializer_class = ITSMServiceSerializer

    @extend_schema(request=ITSMServiceSerializer, responses=None)
    def get_queryset(self):
        queryset = ITSMService.objects.all()
        return queryset


class IncidentStatusListView(generics.ListAPIView):
    """Allows one to get all incident statuses eg Info, Final, Update"""
    serializer_class = IncidentStatusSerializer

    @extend_schema(request=IncidentStatus, responses=None)
    def get_queryset(self):
        queryset = IncidentStatus.objects.all()
        return queryset


class IncidentStatusRetrieveView(generics.RetrieveAPIView):
    """Allows one to get a single Incident status"""
    serializer_class = IncidentStatusSerializer

    @extend_schema(request=IncidentStatus, responses=None)
    def get_queryset(self):
        queryset = IncidentStatus.objects.all()
        return queryset


class EmailDistributionListView(generics.ListAPIView):
    """Retrieve all email distributions eg mpamonitoring@m-pesa.africa"""
    serializer_class = EmailDistributionListSerializer

    @extend_schema(request=EmailDistributionListSerializer, responses=None)
    def get_queryset(self):
        queryset = EmailDistributionList.objects.all()
        return queryset


class EmailDistributionRetrieveView(generics.RetrieveAPIView):
    """Retrieve a single email address"""
    serializer_class = EmailDistributionListSerializer

    @extend_schema(request=EmailDistributionListSerializer, responses=None)
    def get_queryset(self):
        queryset = EmailDistributionList.objects.all()
        return queryset
