from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import RegisterView
from bookings.views import (ReservationCancelView, ReservationDetailView,
                            ReservationListCreateView, ReservationStatusView,
                            TableListView)
from menu.views import CategoryListView, DishDetailView, DishListCreateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Auth
    path('api/register/', RegisterView.as_view()),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),

    # Menu
    path('api/categories/', CategoryListView.as_view()),
    path('api/dishes/', DishListCreateView.as_view()),
    path('api/dishes/<int:pk>/', DishDetailView.as_view()),

    # Bookings
    path('api/tables/', TableListView.as_view()),
    path('api/reservations/', ReservationListCreateView.as_view()),
    path('api/reservations/<int:pk>/', ReservationDetailView.as_view()),
    path('api/reservations/<int:pk>/status/', ReservationStatusView.as_view()),
    path('api/reservations/<int:pk>/cancel/', ReservationCancelView.as_view()),
]
