from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from .models import Patient, Doctor, Department
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate



def register(request):
    if request.method == 'POST':
        # Get data from the form
        name = request.POST.get('name')
        department_id = request.POST.get('department')
        priority = request.POST.get('priority')
        doctor_id = request.POST.get('doctor')

        try:
            # Fetch the Department and Doctor instances
            department = Department.objects.get(id=department_id)
            doctor = Doctor.objects.get(id=doctor_id)

            # Create Patient instance
            patient = Patient.objects.create(name=name, department=department, priority=priority, doctor=doctor)
            messages.success(request, f'Patient {patient.name} registered successfully!')
            return redirect('patient')
        except Department.DoesNotExist:
            messages.error(request, 'The selected department does not exist.')
        except Doctor.DoesNotExist:
            messages.error(request, 'The selected doctor does not exist.')

    # Get list of doctors and departments
    doctors = Doctor.objects.all()
    departments = Department.objects.all()

    return render(request, 'register.html', {'doctors': doctors, 'departments': departments})

def queue_status(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(f"{reverse('login_view')}?next={request.path}")

    # Order patients by priority and registration time and fetch related department data
    patients = Patient.objects.select_related('department').filter(status='waiting').order_by('priority', 'registered_at')

    return render(request, 'queue_status.html', {'patients': patients})





def mark_next_patient(request, id):
    patient = get_object_or_404(Patient, id=id)
    patient.status = 'In Progress'
    patient.save()
    return redirect('queue_status')



def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patient.html', {'patients': patients})

def patient_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        department_id = request.POST.get('department')
        priority = request.POST.get('priority')
        doctor_id = request.POST.get('doctor')
        room_id = request.POST.get('room')
        status = request.POST.get('status')

        department = Department.objects.get(id=department_id)
        doctor = Doctor.objects.get(id=doctor_id)


        Patient.objects.create(name=name, department=department, priority=priority, doctor=doctor, status=status)
        messages.success(request, 'Patient added successfully!')
        return redirect('patient_list')
    else:
        departments = Department.objects.all()
        doctors = Doctor.objects.all()
        return render(request, 'patient.html', {'departments': departments, 'doctors': doctors})


def patient_edit(request, id):
    patient = get_object_or_404(Patient, id=id)
    if request.method == 'POST':
        patient.name = request.POST.get('name')
        patient.department_id = request.POST.get('department')
        patient.priority = request.POST.get('priority')
        patient.doctor_id = request.POST.get('doctor')
        patient.status = request.POST.get('status')  # Ensure status is being set
        patient.save()
        return redirect('patient')
    else:
        departments = Department.objects.all()
        doctors = Doctor.objects.all()
        return render(request, 'edit_patient.html', {'patient': patient, 'departments': departments, 'doctors': doctors})




def patient_delete(request, id):
    try:
     patient = Patient.objects.get(id=id)
     patient.delete()
     messages.success(request, 'Patient deleted successfully!')
    except Patient.DoesNotExist:
       messages.error(request, 'Patient not found.')
    return redirect('patient')

def patient_update(request, id):
    patient = get_object_or_404(Patient, id=id)
    if request.method == 'POST':
        patient.name = request.POST.get('name')
        patient.department_id = request.POST.get('department')
        patient.priority = request.POST.get('priority')
        patient.doctor_id = request.POST.get('doctor')
        patient.room_id = request.POST.get('room')
        patient.status = request.POST.get('status')
        patient.save()
        return redirect('patient_list')





def index(request):
    return render(request, 'index.html', {'navbar': 'home'})


def patient(request):
    patients = Patient.objects.all()
    return render(request, 'patient.html', {'patients': patients})


def about(request):
    return render(request, 'about.html', {'navbar': 'about'})

def contact(request):
    submitted = False
    firstname = ''

    if request.method == 'POST':
        # Get form data from POST request
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        country = request.POST.get('country')
        subject = request.POST.get('subject')

        # After successful submission, set submitted to True
        submitted = True

    return render(request, 'contact.html', {'submitted': submitted, 'firstname': firstname})



def login_view(request):
    if request.method == "POST":
        # Using the AuthenticationForm to validate the credentials
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # If form is valid, authenticate the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {user.username}!")
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid credentials, please try again.")
    else:
        form = AuthenticationForm()

    return render(request, 'login_view.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login_view')

def department_list(request):
    departments = Department.objects.all()
    return render(request, 'department.html', {'departments': departments})
