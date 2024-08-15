from django.db import models
from accounts.models import CustomUser


# Create your models here.
class Market(models.Model):
    market_name = models.CharField(max_length=150),
    market_abbreviation = models.CharField(max_length=50),
    market_timezone = models.CharField(max_length=50)


class IncidentPriority(models.Model):
    incident_priority = models.CharField(max_length=10, unique=True)


class Service(models.Model):
    name = models.CharField(max_length=150)


class ITSMService(models.Model):
    ITSM_name = models.CharField(max_length=150)
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE)
    market_id = models.ForeignKey(Market, on_delete=models.CASCADE)


class SystemServices(models.Model):
    system_service_name = models.CharField(max_length=150)


class EmailDistributionList(models.Model):
    dl_email = models.EmailField()
    distribution_name = models.CharField(max_length=150)


class IncidentStatus(models.Model):
    incident_status = models.CharField(max_length=100)


class Incident(models.Model):
    incident_number = models.CharField(max_length=100),
    incident_summary = models.TextField(),
    incident_priority = models.ForeignKey(IncidentPriority, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    is_cancelled = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    impact_start_time_utc = models.DateTimeField()
    impact_end_time_utc = models.DateTimeField()
    impact_duration = models.DurationField(default=None)
    previous_business_impact = models.TextField()
    current_business_impact = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    market_id = models.ForeignKey(Market, on_delete=models.SET_NULL, null=True)
    service_impacted_id = models.ForeignKey(SystemServices, on_delete=models.SET_NULL, null=True)
    ITSMService_id = models.ForeignKey(ITSMService, on_delete=models.SET_NULL, null=True)
    incident_status = models.ForeignKey(IncidentStatus, on_delete=models.SET_NULL, null=True)


class IncidentUpdate(models.Model):
    incident_id = models.ForeignKey(Incident, on_delete=models.CASCADE)
    # incident_status_id = models.ForeignKey(IncidentStatus, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    update_description = models.TextField()
    # image_attachment = models.ImageField(upload_to='')
