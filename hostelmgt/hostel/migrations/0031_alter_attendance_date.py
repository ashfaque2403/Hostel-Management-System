# Generated by Django 4.2.7 on 2024-01-04 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0030_alter_attendance_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
