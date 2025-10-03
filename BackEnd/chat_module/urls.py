from django.urls import path
from .views import (
    MessageListAPIView,
    MessageCreateAPIView,
    MessageUpdateDeleteAPIView,
    MessageReactionAPIView,
    UnreadMessageCountAPIView,
    SearchMessagesAPIView
)

urlpatterns = [
    # Message CRUD
    path("rooms/<int:room_id>/messages/", MessageListAPIView.as_view(), name="message-list"),
    path("rooms/<int:room_id>/messages/create/", MessageCreateAPIView.as_view(), name="message-create"),
    path("rooms/<int:room_id>/messages/<int:message_id>/", MessageUpdateDeleteAPIView.as_view(), name="message-detail"),
    # Reactions
    path("messages/<int:message_id>/react/", MessageReactionAPIView.as_view(), name="message-react"),
    # Unread count
    path("unread-count/", UnreadMessageCountAPIView.as_view(), name="unread-count"),
    # Search
    path("search/", SearchMessagesAPIView.as_view(), name="message-search"),
]
