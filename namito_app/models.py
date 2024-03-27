from django.db import models

# Create your models here.
from django.utils.text import slugify


class MetaInfo(models.Model):
    data_for = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.data_for)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.data_for}"


class MetaTag(models.Model):
    key = models.CharField(max_length=100)
    value = models.TextField(null=True)
    meta_info = models.ForeignKey(MetaInfo, on_delete=models.CASCADE)