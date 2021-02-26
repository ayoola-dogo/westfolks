from django.db import models
from django.conf import settings
from PIL import Image
import os
from accounts.models import Account
from django.contrib.auth import get_user_model


User = get_user_model()


def change_image_path(image):
    filename = os.path.split(image)[1]
    return filename


# Create your models here.
class Company(models.Model):
    account = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=150, null=True, blank=True)
    logo = models.ImageField(default='default/img/default.png', upload_to='default/img/', null=True)
    mantra = models.TextField(max_length=300, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.company_name)

    # Override the save method
    def save(self, **kwargs):
        super().save()
        img = Image.open(self.logo.path)
        if img.width != 200 and img.height != 200:
            output_size = (200, 200)
            self.initial_path = self.logo.path
            filename = change_image_path(self.logo.path)
            if filename != "default.png":
                pass
    #             self.company_logo.path = os.path.join(settings.MEDIA_ROOT, "{}/img/{}".format(self.account.user.email,
    #                                                                                           filename))
    #             img.resize(output_size, Image.ANTIALIAS).save(self.company_logo.path)
    #             os.remove(self.initial_path)
    #
    # def delete(self, using=None, keep_parents=False):
    #     super().delete()
    #     os.remove(self.company_logo.path)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
