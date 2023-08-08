from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.decorators import login_required



app_name = 'applications'

urlpatterns = [
    path('', views.applications, name='applications'),
    path('applications/approve/<int:id>', views.approve_application, name='approve_application'),
    path('applications/decline/<int:id>', views.decline_application, name='decline_application'),
    path('applications/edit/<int:id>', views.edit_application, name='edit_application'),

    path('applications/new/', views.new, name='new'),

]