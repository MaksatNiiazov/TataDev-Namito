import html
import re
from django.db import models
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel, models.Model):
    CATEGORY_TYPES = [(0, "For men"), (1, "For woman"), (2, "For children"), (3, "Unisex")]
    name = models.CharField(max_length=255)
    type = models.IntegerField(choices=CATEGORY_TYPES, default=3)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    image = models.ImageField(null=True, blank=True)
    parent = TreeForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="children")
    order = models.IntegerField(blank=True, null=True, default=0)
    meta_title = models.CharField(max_length=59, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    class MPTTMeta:
        order_insertion_by = ["order"]

    def save(self, *args, **kwargs):
        base_slug = slugify(self.name)
        counter = 0

        unique_slug = base_slug
        while Category.objects.filter(slug=unique_slug).exists():
            counter += 1
            unique_slug = f"{base_slug}-{counter}"

        self.slug = unique_slug
        super().save(*args, **kwargs)

# class Tag(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    meta_title = models.CharField(max_length=59, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    keywords = models.JSONField(null=True, blank=True)
    # tags = models.ManyToManyField(Tag, related_name='products')

    def first_image(self):
        if self.images.first():
            return self.images.first().image.url

    def generate_meta_description(self):
        if self.description:
            decoded_description = html.unescape(self.description)
            self.description = decoded_description
            first_sentence_match = re.match(r"^(.*?[.!?])", decoded_description)
            first_sentence = first_sentence_match.group(1) if first_sentence_match else decoded_description

            return first_sentence[:160]
        else:
            return ""

    def generate_meta_title(self):
        return self.name

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if not self.meta_description:
            self.meta_description = self.generate_meta_description()

        if not self.meta_title:
            self.meta_title = self.generate_meta_title()
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Color(models.Model):
    name = models.CharField(max_length=50)
    hex_code = models.CharField(max_length=7, blank=True, help_text="HEX color code, e.g., #FFFFFF for white")

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Variant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='variants')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='variants')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.color} - {self.size}"


class Image(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    variant = models.ForeignKey(Variant, related_name='images', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} Image"
