from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from .forms import MyPasswordChangeForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, CompanyForm, UserUpdateForm, EmployeeProfileForm
from .models import EmployerProfile, User

# Create your views here.



def login_view(request):
    if request.POST:
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'You are now logged in as {user.get_full_name()}')
            return redirect('applications:applications')
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'registration/login.html', context)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(data=request.POST)
        company_form = CompanyForm(data=request.POST)

        if user_form.is_valid() and company_form.is_valid():
            user = user_form.save(commit=False)
            company = company_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.user_type = 'Employer'
            user.save()
            profile = EmployerProfile.objects.create(user=user)
            company.employer = profile
            company.save()
            login(request, user)
            messages.success(request, f'You are now logged in as {user.get_full_name()}')
            return redirect('applications:applications')

    else:
        user_form = UserRegistrationForm()
        company_form = CompanyForm()

    context = {
        'user_form': user_form,
        'company_form': company_form
    }

    return render(request, 'registration/register.html', context)

class PasswordChangeView(PasswordChangeView):
    form_class = MyPasswordChangeForm
    template_name = "registration/password_change_form.html"

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Password updated successfully")
        return super(PasswordChangeView, self).form_valid(form)


@login_required
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Changes Saved Successfully")
            return redirect('applications:applications')
        messages.warning(request, "Something happened")
    else:
        form = UserUpdateForm(instance=user)

    context = {
        'form': form,
    }

    return render(request, 'accounts/profile_edit.html', context)



def add_employee(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(data=request.POST)
        profile_form = EmployeeProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)

            user.set_password(user_form.cleaned_data['password'])
            user.user_type = 'Employee'
            user.save()

            profile.user = user
            profile.company = request.user.employer_profile.company
            profile.save()

            messages.success(request, f'Successfully saved {user.get_full_name()}')
            return redirect('accounts:employees')

    else:
        user_form = UserRegistrationForm()
        profile_form = EmployeeProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'accounts/add_employee.html', context)


@login_required
def edit_employee(request, id):
    employee = User.objects.get(id=id)
    employee_profile = employee.employee_profile

    if request.method == 'POST':
        user_form = UserUpdateForm(data=request.POST, instance=employee)
        profile_form = EmployeeProfileForm(data=request.POST, instance=employee_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Changes Saved Successfully")
            return redirect('accounts:employees')
        messages.warning(request, "Something happened")
    else:
        user_form = UserUpdateForm(instance=employee)
        profile_form = EmployeeProfileForm(instance=employee_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'accounts/add_employee.html', context)


@login_required()
def delete_employee(request, id):
    employee = User.objects.get(id=id)
    employee.delete()
    messages.success(request, 'Successfully deleted')
    return redirect('accounts:employees')
    
    
def my_logout(request):
    logout(request)
    return redirect('applications:applications')


@login_required()
def employees(request):
    if request.user.user_type == 'Employer':
        employees = request.user.employer_profile.company.employees.all()
    else:
        messages.warning(request, "You are not allowed to perform that action")
        return redirect('applications:applications')

    context = {
        'employees': employees
    }
    
    return render(request, 'accounts/employees.html', context)