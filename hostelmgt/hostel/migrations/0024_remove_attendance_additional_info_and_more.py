# Generated by Django 4.2.7 on 2023-12-30 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0023_attendance_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='additional_info',
        ),
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
