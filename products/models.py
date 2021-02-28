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
    company = models.ForeignKey(Company, null=False, blank=False, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=120, null=False, blank=False)
    category = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(default='default/img/default.png', upload_to='default/img/', null=True)
    url = models.URLField(max_length=200)

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse('products:product-detail', args=[self.pk, ])

    def get_image_url(self):
        return self.image.path

    # Override the save method
    def save(self, **kwargs):
        super().save()
        img = Image.open(self.image.path)
        if img.width != 800 and img.height != 800:
            output_size = (800, 800)
            img.resize(output_size, Image.ANTIALIAS).save(self.image.path)

    def delete(self, using=None, keep_parents=False):
        super().delete()
        os.remove(self.image.path)
