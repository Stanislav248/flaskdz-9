from django.contrib.auth.models import User
from django.db import models


class Table(models.Model):
    number = models.PositiveIntegerField('Номер столика', unique=True)
    seats = models.PositiveIntegerField('Кількість місць')
    is_available = models.BooleanField('Доступний', default=True)

    def __str__(self):
        return f'Столик №{self.number} ({self.seats} місць)'


class Reservation(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Очікує'
        CONFIRMED = 'confirmed', 'Підтверджено'
        CANCELLED = 'cancelled', 'Скасовано'
        COMPLETED = 'completed', 'Завершено'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='reservations')
    date = models.DateField('Дата')
    time = models.TimeField('Час')
    guests = models.PositiveIntegerField('Кількість гостей')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f'{self.user} - {self.table} - {self.date} {self.time}'
