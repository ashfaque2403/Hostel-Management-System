# Generated by Django 4.2.7 on 2023-12-05 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0008_remove_userprofile_password_userprofile_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
