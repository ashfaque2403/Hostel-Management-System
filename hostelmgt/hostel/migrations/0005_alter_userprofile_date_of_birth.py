# Generated by Django 4.2.7 on 2023-12-04 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0004_userprofile_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]
