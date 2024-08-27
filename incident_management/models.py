from django.db import models
from accounts.models import CustomUser


# Create your models here.
class Market(models.Model):
    market_name = models.CharField(max_length=150)
    market_abbreviation = models.CharField(max_length=50)
    market_timezone = models.CharField(max_length=50)

    def __str__(self):
        return self.market_name



class IncidentPriority(models.Model):
    incident_priority = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.incident_priority



class Service(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name



class ITSMService(models.Model):
    ITSM_name = models.CharField(max_length=150)
    service_id = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    market_id = models.ForeignKey(Market, on_delete=models.CASCADE)

    def __str__(self):
        return self.ITSM_name



class SystemServices(models.Model):
    system_service_name = models.CharField(max_length=150)

    def __str__(self):
        return self.system_service_name



class EmailDistributionList(models.Model):
    dl_email = models.EmailField()
    distribution_name = models.CharField(max_length=150)

    def __str__(self):
        return self.dl_email



class IncidentStatus(models.Model):
    incident_status = models.CharField(max_length=100)

    def __str__(self):
        return self.incident_status



class Incident(models.Model):
    incident_number = models.CharField(max_length=100,unique=True)
    incident_summary = models.TextField()
    incident_priority = models.ForeignKey(IncidentPriority, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    is_cancelled = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    impact_start_time_utc = models.DateTimeField()
    impact_end_time_utc = models.DateTimeField(default=None)
    impact_duration = models.DurationField(default=None)
    previous_business_impact = models.TextField(default=None)
    current_business_impact = models.TextField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    market_id = models.ForeignKey(Market, on_delete=models.SET_NULL, null=True)
    service_impacted_id = models.ForeignKey(SystemServices, on_delete=models.SET_NULL, null=True)
    ITSMService_id = models.ForeignKey(ITSMService, on_delete=models.SET_NULL, null=True)
    incident_status = models.ForeignKey(IncidentStatus, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.incident_number



class IncidentUpdate(models.Model):
    incident_id = models.ForeignKey(Incident, on_delete=models.CASCADE)
    # incident_status_id = models.ForeignKey(IncidentStatus, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    update_description = models.TextField()
    # image_attachment = models.ImageField(upload_to='')

    def __str__(self):
        return self.incident_id.incident_number

