from django.urls import path
from .views import (
    AssistantConversationListCreateAPIView,
    AssistantConversationDetailAPIView,
    AssistantChatAPIView
)

urlpatterns = [
    path('conversations/', AssistantConversationListCreateAPIView.as_view(), name='conversation-list-create'),
    path('conversations/<int:id>/', AssistantConversationDetailAPIView.as_view(), name='conversation-detail'),
    path('conversations/<int:id>/chat/', AssistantChatAPIView.as_view(), name='assistant-chat'),
]
