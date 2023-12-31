# Generated by Django 4.2.4 on 2023-08-07 08:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='id_number',
        ),
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
        migrations.RemoveField(
            model_name='user',
            name='sex',
        ),
        migrations.CreateModel(
            name='EmployerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employer_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(default='Employer', max_length=50)),
                ('id_number', models.CharField(max_length=50)),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='accounts.company')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='company',
            name='employer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.employerprofile'),
        ),
    ]
