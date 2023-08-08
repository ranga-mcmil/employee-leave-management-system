from django.contrib import admin
from .models import User, Company, EmployerProfile, EmployeeProfile
from import_export.admin import ExportActionMixin


# Register your models here.
@admin.register(User)
class UserAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'user_type')
    list_filter = ('user_type',)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'employer',)


@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',)

@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('id', 'user', 'role', 'id_number', 'sex', 'company')
    list_filter = ('company',)