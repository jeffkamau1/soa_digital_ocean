from django.contrib import admin

# Register your models here.
from accounts.models import CustomUser, Role


class CustomUserAdmin(admin.ModelAdmin):
    list_filter = ['is_staff', 'is_superuser', 'is_verified', 'role']
    search_fields = ['email']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Role)
