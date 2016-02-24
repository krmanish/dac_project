# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AvailableDay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.CharField(help_text=b'Day as Monday/Tuesday', max_length=20)),
                ('short_name', models.CharField(help_text=b'Abbreviation of week days like Mon/Tue ', max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='AvailableTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.PositiveSmallIntegerField(help_text=b'All available time in 24 hour format')),
            ],
        ),
        migrations.CreateModel(
            name='BookingStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_ts', models.DateTimeField(help_text=b'Created timespan', auto_now_add=True)),
                ('updated_ts', models.DateTimeField(help_text=b'Updated timestamp', auto_now=True)),
                ('booked_date', models.DateField(help_text=b'Start Date')),
                ('no_of_days', models.PositiveSmallIntegerField(help_text=b'Number of Days')),
                ('duration', models.PositiveSmallIntegerField(help_text=b'Duration In Hours')),
                ('booked_time', models.ForeignKey(help_text=b'Start time in 24 hour format', to='doctor.AvailableTime')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_ts', models.DateTimeField(help_text=b'Created timespan', auto_now_add=True)),
                ('updated_ts', models.DateTimeField(help_text=b'Updated timestamp', auto_now=True)),
                ('specialist', models.CharField(default=b'GP', max_length=5, choices=[(b'GP', b'General Physician'), (b'ES', b'Eye Specialist'), (b'ORT', b'Orthopedics'), (b'NRS', b'Neurosurgeon')])),
                ('gender', models.CharField(default=b'F', max_length=10, choices=[(b'M', b'Male'), (b'F', b'Female'), (b'O', b'Other')])),
                ('address', models.TextField(null=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DoctorSchedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_ts', models.DateTimeField(help_text=b'Created timespan', auto_now_add=True)),
                ('updated_ts', models.DateTimeField(help_text=b'Updated timestamp', auto_now=True)),
                ('is_active', models.BooleanField(default=True, help_text=b'Active/Inactive Flag')),
                ('day', models.ForeignKey(help_text=b'Day', to='doctor.AvailableDay')),
                ('doctor', models.ForeignKey(to='doctor.Doctor')),
                ('end_time', models.ForeignKey(related_name='end_time', to='doctor.AvailableTime')),
                ('start_time', models.ForeignKey(related_name='start_time', to='doctor.AvailableTime')),
            ],
        ),
        migrations.AddField(
            model_name='bookingstatus',
            name='schedule',
            field=models.ForeignKey(to='doctor.DoctorSchedule'),
        ),
        migrations.AlterUniqueTogether(
            name='doctorschedule',
            unique_together=set([('doctor', 'day', 'start_time')]),
        ),
    ]
