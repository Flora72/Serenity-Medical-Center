from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Patient(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    priority = models.CharField(max_length=50)
    doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=100, blank=True, null=True)

    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('in_queue', 'In Queue'),
        ('under_observation', 'Under Observation'),
        ('discharged', 'Discharged'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    medical_history = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.department.name if self.department else 'N/A'} ({self.priority})"




class QueueStatus(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)  # ForeignKey reference to Patient model
    status = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.name} - {self.status} ({self.timestamp})"


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Dr. {self.name} ({self.department.name if self.department else 'N/A'})"



