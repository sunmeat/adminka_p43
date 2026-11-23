from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255)
    birth_year = models.IntegerField(default=1960)
    rating = models.FloatField()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    pages = models.IntegerField(default=100)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=100)
    published_year = models.IntegerField(default=2026)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.title