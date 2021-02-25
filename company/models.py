from django.db import models
from django.conf import settings
from PIL import Image
import os


# Create your models here.
class Company(models.Model):
    company_name = models.CharField(max_length=150)
    company_logo = models.ImageField(default=settings.STATIC_ROOT + 'assets/img/default.png',
                                     upload_to='user_profiles/images/', null=True)
    company_mantra = models.TextField(max_length=300, null=True, blank=True)
    company_description = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.company_name)

    # Override the save method
    def save(self):
        super().save()
        img = Image.open(self.company_logo.path)
        if img.width != 200 and img.height != 200:
            output_size = (200, 200)
            img.resize(output_size, Image.ANTIALIAS).save(self.company_logo.path)

    def delete(self, using=None, keep_parents=False):
        super().delete()
        if self.company_logo.path != os.path.join(settings.STATIC_ROOT, 'assets/img/default.png'):
            os.remove(self.company_logo.path)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
