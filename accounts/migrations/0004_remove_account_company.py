# Generated by Django 3.0.3 on 2021-02-26 01:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_account_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='company',
        ),
    ]
