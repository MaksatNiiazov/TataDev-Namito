from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name


# class Tag(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    # tags = models.ManyToManyField(Tag, related_name='products')

    def __str__(self):
        return self.name


class Variant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    color = models.CharField(max_length=30)
    size = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.color} - {self.size}"


class Image(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    variant = models.ForeignKey(Variant, related_name='images', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} Image"
