from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    friendly_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="products"
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    # Image handling
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(upload_to="products/", null=True, blank=True)

    def __str__(self):
        return self.name

