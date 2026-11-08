from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser

from .models import Category, Dish
from .serializers import CategorySerializer, DishSerializer


class CategoryListView(generics.ListAPIView):
    """Список категорій (доступно всім)."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class DishListCreateView(generics.ListCreateAPIView):
    """GET - список страв (всім). POST - додати страву (тільки адмін)."""
    queryset = Dish.objects.select_related('category').all()
    serializer_class = DishSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]


class DishDetailView(generics.RetrieveAPIView):
    """Одна страва (доступно всім)."""
    queryset = Dish.objects.select_related('category').all()
    serializer_class = DishSerializer
    permission_classes = [AllowAny]
