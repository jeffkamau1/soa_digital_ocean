from django.contrib import admin
from incident_management.models import (
    Market,
    Incident,
    IncidentStatus,
    IncidentPriority,
    IncidentUpdate,
    ITSMService,
    Service,
    SystemServices,
    EmailDistributionList)


# Register your models here.
class IncidentAdmin(admin.ModelAdmin):
    list_filter = ['incident_priority','incident_status', 'is_completed', 'is_cancelled', 'created_by']
    search_fields = ['incident_number', 'incident_summary']


admin.site.register(Incident, IncidentAdmin)
admin.site.register(IncidentPriority)
admin.site.register(Market)
admin.site.register(IncidentStatus)
admin.site.register(IncidentUpdate)
admin.site.register(ITSMService)
admin.site.register(Service)
admin.site.register(SystemServices)
admin.site.register(EmailDistributionList)
