from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.db.models import Q
from .models import User, FriendRequest
from .serializers import (
    UserSerializer,
    FriendRequestSerializer,
    UserSignupSerializer,
    UserLoginSerializer,
    FriendRequestDataSerializer,
)
from django.contrib.auth import authenticate, login
from rest_framework import filters


class UserSearchAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        search_keyword = self.request.query_params.get("search", "")
        return User.objects.filter(
            Q(email__iexact=search_keyword) | Q(username__icontains=search_keyword)
        ).exclude(id=self.request.user.id)


class UserSignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Log the user in after signup
        login(request, user)

        return Response(
            {"user_id": user.id, "email": user.email}, status=status.HTTP_201_CREATED
        )


class UserLoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(request, **serializer.validated_data)

        if user:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {"token": token.key, "user_id": user.id, "email": user.email}
            )
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class FriendRequestCreateAPIView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user, status="pending")
        friend_identifier = self.request.data.get("to_user")
        try:
            friend = User.objects.get(email=friend_identifier)
        except User.DoesNotExist:
            try:
                friend = User.objects.get(username=friend_identifier)
            except User.DoesNotExist:
                return Response(
                    {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )

        serializer.instance.to_user = friend
        serializer.instance.save()

        return Response(
            {"message": "Friend request sent successfully"},
            status=status.HTTP_201_CREATED,
        )


class PendingFriendRequestsAPIView(generics.ListAPIView):
    serializer_class = FriendRequestDataSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(
            from_user=self.request.user, status="pending"
        )


class UpdateFriendRequestStatusAPIView(generics.UpdateAPIView):
    serializer_class = FriendRequestDataSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(from_user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

class ListFriendsAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        friend_requests = FriendRequest.objects.filter(from_user=self.request.user, status='accepted')
        friend_users = [request.to_user for request in friend_requests]
        return friend_users