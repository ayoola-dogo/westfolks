from django.db import models
from PIL import Image
from company.models import Company
from django.shortcuts import reverse
import os
from django.conf import settings
from django.template.defaultfilters import slugify
from string import ascii_letters
import random


def change_image_path(image):
    filename = os.path.split(image)[1]
    return filename


# Create your models here.
class Product(models.Model):
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=120, null=True, blank=True)
    slug = models.SlugField(null=False, blank=False)
    category = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    # Could use a setter to set this field
    image = models.ImageField(default='default/img/default.png', upload_to='default/img/', null=True)
    url = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse('products:product-detail', args=[self.slug, ])

    def get_image_url(self):
        return self.image.path

    def get_slug(self):
        return self.slug

    # Override the save method
    def save(self, *args, **kwargs):
        if not self.id:
            slug_str = "{}-{}".format(''.join(random.choice(ascii_letters) for i in range(7)), self.product_name)
            self.slug = slugify(slug_str)
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.width != 800 and img.height != 800:
            output_size = (800, 800)
            img.resize(output_size, Image.ANTIALIAS).save(self.image.path)

    def delete(self, using=None, keep_parents=False):
        super().delete()
        os.remove(self.image.path)
