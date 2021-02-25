from django.db import models
from accounts.models import Account
from django.conf import settings
from PIL import Image
import os


def change_image_path(image):
    filename = os.path.split(image)[1]
    return filename


# Create your models here.
class Company(models.Model):
    # The account field reference the account model not the instance
    account = models.OneToOneField(Account, null=True, blank=False, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=150)
    company_logo = models.ImageField(default='default/img/default.png', upload_to='default/img/', null=True)
    company_mantra = models.TextField(max_length=300, null=True, blank=True)
    company_description = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.company_name)

    # Override the save method
    def save(self, **kwargs):
        super().save()
        img = Image.open(self.company_logo.path)
        if img.width != 200 and img.height != 200:
            output_size = (200, 200)
            self.initial_path = self.company_logo.path
            filename = change_image_path(self.company_logo.path)
            print(self.account.user.email)
            if filename != "default.png":
                self.company_logo.path = os.path.join(settings.MEDIA_ROOT, "{}/img/{}".format(self.account.user.email,
                                                                                              filename))
                img.resize(output_size, Image.ANTIALIAS).save(self.company_logo.path)
                os.remove(self.initial_path)

    def delete(self, using=None, keep_parents=False):
        super().delete()
        os.remove(self.company_logo.path)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
