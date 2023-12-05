from django.urls import path
from .views import (
    UserSearchAPIView,
    UserSignupView,
    UserLoginView,
    FriendRequestCreateAPIView,
    PendingFriendRequestsAPIView,
    UpdateFriendRequestStatusAPIView,
    ListFriendsAPIView,
)

urlpatterns = [
    path("user-search/", UserSearchAPIView.as_view(), name="user-search"),
    path("signup/", UserSignupView.as_view(), name="user-signup"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path(
        "friend-request/", FriendRequestCreateAPIView.as_view(), name="friend-request"
    ),
    path(
        "pending-friend-requests/",
        PendingFriendRequestsAPIView.as_view(),
        name="pending-friend-requests",
    ),
    path(
        "update-friend-request-status/<int:pk>/",
        UpdateFriendRequestStatusAPIView.as_view(),
        name="update-friend-request-status",
    ),
    path("list-friends/", ListFriendsAPIView.as_view(), name="list-friends"),
]
