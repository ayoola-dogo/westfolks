# Generated by Django 3.0.3 on 2021-02-26 01:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_account_company'),
        ('company', '0013_auto_20210226_0023'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Account'),
        ),
    ]
