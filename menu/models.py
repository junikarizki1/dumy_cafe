from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, help_text="Gunakan huruf kecil, tanpa spasi, contoh: minuman-kopi")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class ListMenu(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, help_text="Teks unik untuk URL, akan terisi otomatis jika dikosongkan.")
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="list_menu")
    
    def __str__(self):
        return self.name