from django.db import models
from PIL import Image
from company.models import Company
from django.shortcuts import reverse
import os
from django.conf import settings


def change_image_path(image):
    filename = os.path.split(image)[1]
    return filename


# Create your models here.
class Product(models.Model):
    company = models.ForeignKey(Company, null=True, blank=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.TextField(null=True, blank=True)
    image = models.ImageField(default='default/img/default.png', upload_to='default/img/', null=True)
    url = models.URLField(max_length=200)

    class Meta:
        unique_together = ('name',)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('single_product', args=[self.name, ])

    # Override the save method
    def save(self, **kwargs):
        super().save()
        img = Image.open(self.image.path)
        if img.width != 250 and img.height != 350:
            output_size = (250, 350)
            self.initial_path = self.image.path
            filename = change_image_path(self.image.path)
            print(self.company.account.user.email)
            if filename != "default.png":
                self.image.path = os.path.join(settings.MEDIA_ROOT, "{}/img/{}".format(self.company.account.user.email,
                                                                                              filename))
                img.resize(output_size, Image.ANTIALIAS).save(self.image.path)
                os.remove(self.initial_path)

    def delete(self, using=None, keep_parents=False):
        super().delete()
        os.remove(self.image.path)
