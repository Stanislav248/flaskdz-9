from django.db import models


class Category(models.Model):
    name = models.CharField('Назва', max_length=100, unique=True)
    description = models.TextField('Опис', blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField('Назва', max_length=150)
    description = models.TextField('Опис', blank=True)
    price = models.DecimalField('Ціна', max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='dishes')
    is_available = models.BooleanField('Доступна', default=True)

    def __str__(self):
        return self.name
