from django.urls import path
from incident_management.api.views import (
    IncidentCreateView,
    IncidentUpdateView,
    IncidentPriorityListView,
    IncidentPriorityRetrieveView,
    IncidentListView,
    ServiceListView,
    SystemServicesListView,
    ServiceRetrieveView,
    IncidentRetrieveView,
    IncidentCommentRetrieveUpdateView,
    IncidentStatusListView,
    EmailDistributionListView,
    SystemServicesRetrieveView,
    IncidentStatusRetrieveView,
    EmailDistributionRetrieveView,
    ITSMServiceListView,
    ITSMServiceRetrieveView,
    IncidentCommentUpdateListView,
    IncidentCommentUpdateCreateView
)

urlpatterns = [
    path('incident/', IncidentCreateView.as_view(), name='incident_create_view'),
    path('incident/', IncidentListView.as_view(), name='incident_list_view'),
    path('incident/<int:pk>', IncidentRetrieveView.as_view(), name='incident_detail_view'),
    path('incident/<int:pk>', IncidentUpdateView.as_view(), name='incident_update_view'),
    path('incident-priority/', IncidentPriorityListView.as_view(), name='incident_priority_list'),
    path('incident-priority/<int:pk>', IncidentPriorityRetrieveView.as_view(), name='incident_priority_retrieve'),
    path('service/', ServiceListView.as_view(), name='service_list_view'),
    path('service/<int:pk>', ServiceRetrieveView.as_view(), name='service_retrieve_view'),
    path('system-service/', SystemServicesListView.as_view(), name='service_list_view'),
    path('system-service/<int:pk>', SystemServicesRetrieveView.as_view(), name='system_service_retrieve_view'),
    path('incident-status', IncidentStatusListView.as_view(), name='incident_status_list_view'),
    path('incident-status/<int:pk>', IncidentStatusRetrieveView.as_view(), name='incident_status_retrieve_view'),
    path('incident/<int:pk>/incident-update', IncidentCommentUpdateCreateView.as_view(), name='incident_comment_update_create_view'),
    path('incident/<int:incident_id>/incident-update/<int:pk>', IncidentCommentRetrieveUpdateView.as_view(), name='incident_comment_update_view'),
    path('incident/<int:pk>/incident-update', IncidentCommentUpdateListView.as_view(), name='incident_comment_update_create_view'),
    path('email-distribution/', EmailDistributionListView.as_view(), name='email_distribution_list_view'),
    path('email-distribution/<int:pk>', EmailDistributionRetrieveView.as_view(), name='email_distribution_retrieve_view'),
    path('itsm-service/', ITSMServiceListView.as_view(), name='ITSMServiceList_view'),
    path('itsm-service/<int:pk>', ITSMServiceRetrieveView.as_view(), name='ITSMRetrieve_view')
]
