from django.contrib import admin
from .models import Reservation, Table

admin.site.register(Table)
admin.site.register(Reservation)
