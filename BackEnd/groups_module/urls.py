from django.urls import path
from .views import (
    GroupListCreateAPIView,
    GroupDetailAPIView,
    GroupMembershipListCreateAPIView,
    GroupMembershipDetailAPIView,
    UserChatRoomsAPIView
)

urlpatterns = [
    path('groups/', GroupListCreateAPIView.as_view(), name='group-list-create'),
    path('groups/<int:group_id>/', GroupDetailAPIView.as_view(), name='group-detail'),
    path('groups/<int:group_id>/members/', GroupMembershipListCreateAPIView.as_view(), name='membership-list-create'),
    path('groups/<int:group_id>/members/<int:membership_id>/', GroupMembershipDetailAPIView.as_view(), name='membership-detail'),
    path('my-chatrooms/', UserChatRoomsAPIView.as_view(), name='user-chatrooms'),
]