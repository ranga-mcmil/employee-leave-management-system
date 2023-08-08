from django.contrib import admin
from .models import Application
from import_export.admin import ExportActionMixin


# Register your models here.
@admin.register(Application)
class ApplicationAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('id', 'status', 'start_date', 'end_date', 'employee', 'date_created')
    list_filter = ('status', 'employee')