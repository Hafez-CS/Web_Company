from django.urls import path
from .views import MessageCreateAPIView, MessageListAPIView

urlpatterns = [
    path('messages/', MessageListAPIView.as_view(), name="message_list"),
    path('messages/send/', MessageCreateAPIView.as_view(), name="message_create")
]
