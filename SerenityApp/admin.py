from django.contrib import admin
from .models import Patient, Doctor, Department

class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'priority', 'status', 'doctor')
    list_filter = ('department', 'priority', 'status')
    search_fields = ('name', 'department__name', 'priority', 'status')

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')
    list_filter = ('department',)
    search_fields = ('name', 'department__name')

admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Department, DepartmentAdmin)
