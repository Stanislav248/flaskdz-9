from datetime import date

from rest_framework import serializers

from .models import Reservation, Table


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'number', 'seats', 'is_available']


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'user', 'table', 'date', 'time', 'guests', 'status']
        read_only_fields = ['status']

    def validate_date(self, value):
        if value < date.today():
            raise serializers.ValidationError('Не можна бронювати на минулу дату.')
        return value

    def validate(self, data):
        table = data['table']
        if not table.is_available:
            raise serializers.ValidationError('Цей столик недоступний.')
        if data['guests'] > table.seats:
            raise serializers.ValidationError(
                f'За столиком лише {table.seats} місць.')
        busy = Reservation.objects.filter(
            table=table, date=data['date'], time=data['time']
        ).exclude(status=Reservation.Status.CANCELLED)
        if busy.exists():
            raise serializers.ValidationError('Столик уже заброньовано на цей час.')
        return data


class ReservationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['status']
