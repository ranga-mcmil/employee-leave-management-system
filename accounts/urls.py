from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.decorators import login_required



app_name = 'accounts'

urlpatterns = [
   path('register/', views.register, name='register'),
   path('login/', views.login_view, name='login'),
   path('logout/', views.my_logout, name='logout'),
   path('profile_edit/', views.profile_edit, name='profile_edit'),
   path('employees/', views.employees, name='employees'),
   path('employees/new/', views.add_employee, name='add_employee'),
   path('employees/delete/<int:id>/', views.delete_employee, name='delete_employee'),
   path('employees/edit/<int:id>/', views.edit_employee, name='edit_employee'),
   path('password_change/', login_required(views.PasswordChangeView.as_view(success_url = '/accounts/')), name='password_change'),
]