from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models.signals import post_save
import os
from shutil import copy2

User = get_user_model()


# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{} Account'.format(self.user)


def create_account(sender, **kwargs):
    if kwargs['created']:
        account = Account.objects.create(user=kwargs['instance'])

        # Create user account directory for file management
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path1 = os.path.join(BASE_DIR, 'static/media/{}/img/logo/'.format(kwargs['instance'].email))
        path2 = os.path.join(BASE_DIR, 'static/media/{}/img/products/'.format(kwargs['instance'].email))
        path3 = os.path.join(BASE_DIR, 'static/media/{}/resources/'.format(kwargs['instance'].email))

        try:
            os.makedirs(path1)
            os.makedirs(path2)
            os.makedirs(path3)
        except OSError:
            print("Creation of the directory {} failed could be due to directory already exist".format(path1))
        else:
            print("Successfully created the directories")

        # copy2(os.path.join(BASE_DIR, 'static/static_root/assets/img/default.png'), path1)


post_save.connect(create_account, sender=User)
