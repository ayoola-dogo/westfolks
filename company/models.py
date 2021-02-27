from django.db import models
from django.conf import settings
from PIL import Image
import os
from accounts.models import Account
from django.contrib.auth import get_user_model


def change_image_path(image):
    filename = os.path.split(image)[1]
    dir_path = os.path.split(image)[1]
    return dir_path, filename


# Create your models here.
class Company(models.Model):
    account = models.OneToOneField(Account, null=False, blank=False, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=150, null=True, blank=True)
    logo = models.ImageField(default='default/img/default.png', upload_to="default/img/", null=True)
    mantra = models.TextField(max_length=300, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.company_name)

    def get_logo_url(self):
        return self.logo.path

    # Override the save method
    def save(self, **kwargs):
        super().save()
        img = Image.open(self.logo.path)
        if img.width != 800 and img.height != 800:
            output_size = (800, 800)
            img.resize(output_size, Image.ANTIALIAS).save(self.logo.path)

    def delete(self, using=None, keep_parents=False):
        super().delete()
        dir_path, filename = change_image_path(self.logo.path)
        if str(filename) != "default.png":
            os.remove(self.logo.path)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
