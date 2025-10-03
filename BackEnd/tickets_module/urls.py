from django.urls import path
from .views import (
    TicketListCreateAPIView,
    TicketDetailAPIView,
    TicketResponseCreateAPIView
)

urlpatterns = [
    path('tickets/', TicketListCreateAPIView.as_view(), name='ticket-list-create'),
    path('tickets/<int:id>/', TicketDetailAPIView.as_view(), name='ticket-detail'),
    path('tickets/<int:id>/responses/', TicketResponseCreateAPIView.as_view(), name='ticket-response-create'),
]
