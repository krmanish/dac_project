# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookingstatus',
            name='booked_time',
        ),
        migrations.RemoveField(
            model_name='bookingstatus',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='bookingstatus',
            name='no_of_days',
        ),
        migrations.AddField(
            model_name='bookingstatus',
            name='end_time',
            field=models.ForeignKey(related_name='book_end_time', default=1, to='doctor.AvailableTime', help_text=b'End time in 24 hour format'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bookingstatus',
            name='start_time',
            field=models.ForeignKey(related_name='book_start_time', default=1, to='doctor.AvailableTime', help_text=b'Start time in 24 hour format'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bookingstatus',
            name='booked_date',
            field=models.DateField(help_text=b'Booked Date'),
        ),
    ]
