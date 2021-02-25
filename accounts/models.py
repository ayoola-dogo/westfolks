from django.db import models
from django.contrib.auth import get_user_model
from company.models import Company
from django.urls import reverse
from django.db.models.signals import post_save
import os

User = get_user_model()


# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.OneToOneField(Company, on_delete=models.SET_NULL, null=True)
    website_url = models.URLField()

    def __str__(self):
        return '{} Account'.format(self.user)


def create_account(sender, **kwargs):
    if kwargs['created']:
        account = Account.objects.create(user=kwargs['instance'])

        # Create user account directory for file management
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path1 = os.path.join(BASE_DIR, 'static/media/{}'.format(kwargs['instance'].email))

        try:
            os.makedirs(path1)
        except OSError:
            print("Creation of the directory {} failed could be due to directory already exist".format(path1))
        else:
            print("Successfully created the directories")


post_save.connect(create_account, sender=User)
