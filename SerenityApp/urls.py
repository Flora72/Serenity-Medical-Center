from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('home/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('queue_status/', views.queue_status, name='queue_status'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('patient/', views.patient_list, name='patient'),
    path('logout_view/', views.logout_view, name='logout_view'),
    path('department/', views.department_list, name='department'),
    path('patients/add/', views.patient_add, name='patient_add'),
    path('patients/<int:id>/delete/', views.patient_delete, name='patient_delete'),
    path('patients/<int:id>/next/', views.mark_next_patient, name='mark_next_patient'),
    path('patients/<int:id>/edit/', views.patient_edit, name='patient_edit'),
    path('patients/<int:id>/update/', views.patient_update, name='patient_update'),
]

