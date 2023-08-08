from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Application
from .forms import ApplicationForm


# Create your views here.
@login_required()
def home(request):
    context = {

    }
    
    return render(request, 'applications/home.html', context)

@login_required()
def new(request):
    if request.user.user_type == 'Employer':
        messages.warning(request, 'Employer cannot apply for leave')
        return redirect('applications:applications')

    if request.method == 'POST':
        form = ApplicationForm(data=request.POST)

        if form.is_valid():
            application = form.save(commit=False)
            application.employee = request.user.employee_profile
            application.company = request.user.employee_profile.company
            application.save()
            messages.success(request, f'Successfully saved')
            return redirect('applications:applications')

    else:
        form = ApplicationForm()

    context = {
        'form': form,
    }
    
    return render(request, 'applications/new.html', context)


@login_required()
def applications(request):
    if request.user.user_type == 'Employer':
        applications = Application.objects.filter(company=request.user.employer_profile.company).order_by('-id')
    elif request.user.user_type == 'Employee':
        applications = Application.objects.filter(employee=request.user.employee_profile).order_by('-id')
    else:
        messages.warning(request, "You are not allowed to perform that action")
        return redirect('accounts:applications')

    context = {
        'applications': applications
    }
    
    return render(request, 'applications/applications.html', context)


@login_required
def edit_application(request, id):
    application = Application.objects.get(id=id)

    print('>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<')
    print('>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<')
    print(application.get_remaining_days())
    print('>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<')
    print('>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<')


    if request.user.user_type == 'Employer' or application.status != 'Pending':
        messages.warning(request, "You cannot edit this application")
        return redirect('applications:applications')

    if request.method == 'POST':
        form = ApplicationForm(data=request.POST, instance=application)

        if form.is_valid():
            form.save()
            messages.success(request, "Changes Saved Successfully")
            return redirect('applications:applications')
        messages.warning(request, "Something happened")
    else:
        form = ApplicationForm(instance=application)

    context = {
        'form': form,
    }

    return render(request, 'applications/new.html', context)


def approve_application(request, id):
    application = Application.objects.get(id=id)
    application.status = 'Approved'
    application.save()
    messages.success(request, "Application Approved")
    return redirect(request.META['HTTP_REFERER'])


def decline_application(request, id):
    application = Application.objects.get(id=id)
    application.status = 'Declined'
    application.save()
    messages.warning(request, "Application Declined")
    return redirect(request.META['HTTP_REFERER'])