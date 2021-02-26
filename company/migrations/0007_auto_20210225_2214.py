# Generated by Django 3.0.3 on 2021-02-25 22:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_account_company'),
        ('company', '0006_auto_20210225_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='account',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Account'),
        ),
    ]
