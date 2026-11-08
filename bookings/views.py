from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Reservation, Table
from .serializers import (ReservationSerializer, ReservationStatusSerializer,
                          TableSerializer)


class TableListView(generics.ListAPIView):
    """Список столиків (щоб знати, який id вказувати при бронюванні)."""
    queryset = Table.objects.filter(is_available=True)
    serializer_class = TableSerializer
    permission_classes = [AllowAny]


class ReservationListCreateView(generics.ListCreateAPIView):
    """GET - мої бронювання. POST - створити бронювання."""
    serializer_class = ReservationSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Reservation.objects.none()
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OwnReservationMixin:
    """Користувач бачить лише свої бронювання, адмін - усі."""
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Reservation.objects.none()
        qs = Reservation.objects.all()
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)


class ReservationDetailView(OwnReservationMixin, generics.RetrieveAPIView):
    """Деталі бронювання."""
    serializer_class = ReservationSerializer


class ReservationStatusView(OwnReservationMixin, generics.UpdateAPIView):
    """Зміна статусу. Адмін - будь-який статус, клієнт - лише 'cancelled'."""
    serializer_class = ReservationStatusSerializer
    http_method_names = ['patch']

    def perform_update(self, serializer):
        new_status = serializer.validated_data['status']
        if not self.request.user.is_staff and new_status != Reservation.Status.CANCELLED:
            raise PermissionDenied('Ви можете лише скасувати бронювання.')
        serializer.save()


class ReservationCancelView(OwnReservationMixin, APIView):
    """Скасування бронювання."""
    permission_classes = [IsAuthenticated]

    @extend_schema(request=None, responses=ReservationSerializer)
    def post(self, request, pk):
        reservation = generics.get_object_or_404(self.get_queryset(), pk=pk)
        if reservation.status == Reservation.Status.CANCELLED:
            return Response({'detail': 'Бронювання вже скасовано.'},
                            status=status.HTTP_400_BAD_REQUEST)
        reservation.status = Reservation.Status.CANCELLED
        reservation.save()
        return Response(ReservationSerializer(reservation).data)
