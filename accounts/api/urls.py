from django.urls import path
from accounts.api.views import (
    register_user_view,
    user_login,
    verify_email,
    ListUsers,
    ListRoles,
    RetrieveUsers,
    RetrieveRoles,
    email_template,
    NonVerifiedUsersListView,
    NonVerifiedUsersRetrieveView,
    VerifyUserView)

urlpatterns = [
    path('register/', register_user_view, name='register'),
    path('login/', user_login, name='login'),
    path('verify-email/<str:token>/', verify_email, name='verify_email'),
    path('nonverified-users/', NonVerifiedUsersListView.as_view(), name='non_verified_users'),
    path('nonverified-users/<int:pk>/', NonVerifiedUsersRetrieveView.as_view(), name='retrieve_non_verified_user'),
    path('verify-user/<int:pk>/', VerifyUserView.as_view(), name='verify_user'),
    path('roles/', ListRoles.as_view(), name='list_roles'),
    path('roles/<int:pk>/', RetrieveRoles.as_view(), name='retrieve_roles'),
    path('users/', ListUsers.as_view(), name='list_users'),
    path('users/<int:pk>/', RetrieveUsers.as_view(), name='retrieve_user'),
    path('emailpage/', email_template, name='email_template', )

]
