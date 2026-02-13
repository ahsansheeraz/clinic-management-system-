from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Patient
from .forms import PatientForm
from users.decorators import role_required
from users.utils import log_action

ALLOWED_ROLES = ['admin', 'superuser', 'call_agent', 'fdo']

@role_required(ALLOWED_ROLES)
def patient_list(request):

    query = request.GET.get('q')  # get search query

    if query:
        patients = Patient.objects.filter(
            is_deleted=False,
            phone__icontains=query
        )
    else:
        patients = Patient.objects.filter(is_deleted=False)

    return render(request, "patients/patient_list.html", {
        "patients": patients,
        "query": query
    })


@role_required(ALLOWED_ROLES)
def patient_add(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.created_by = request.user
            patient.save()

            # Log creation
            log_action(
                user=request.user,
                action_type='create',
                table_name='Patient',
                record_id=patient.id,
                new_value=str(form.cleaned_data)
            )

            messages.success(request, "Patient added successfully.")
            return redirect('patients:patient_list')
    else:
        form = PatientForm()
    return render(request, 'patients/patient_form.html', {'form': form, 'title': 'Add Patient'})

@role_required(ALLOWED_ROLES)
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            old_data = str({
                'name': patient.name,
                'phone': patient.phone,
                'age': patient.age,
                'gender': patient.gender,
                'location': patient.location
            })
            patient = form.save()

            # Log update
            log_action(
                user=request.user,
                action_type='update',
                table_name='Patient',
                record_id=patient.id,
                old_value=old_data,
                new_value=str(form.cleaned_data)
            )

            messages.success(request, "Patient updated successfully.")
            return redirect('patients:patient_list')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/patient_form.html', {'form': form, 'title': 'Edit Patient'})

@role_required(ALLOWED_ROLES)
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patient.is_deleted = True
    patient.deleted_at = timezone.now()
    patient.deleted_by = request.user
    patient.save()

    # Log deletion
    log_action(
        user=request.user,
        action_type='delete',
        table_name='Patient',
        record_id=patient.id,
        old_value=str({
            'name': patient.name,
            'phone': patient.phone,
            'age': patient.age,
            'gender': patient.gender,
            'location': patient.location
        })
    )

    messages.success(request, "Patient deleted successfully.")
    return redirect('patients:patient_list')
