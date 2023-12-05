from rest_framework import serializers
from .models import User, FriendRequest


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    to_user = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = FriendRequest
        fields = ["to_user", "status", "created_at", "from_user"]
        read_only_fields = ["from_user"]

    def validate(self, data):
        from_user = self.context["request"].user
        to_user_identifier = data.get("to_user")
        if not to_user_identifier:
            raise serializers.ValidationError(
                "The 'friend_identifier' field is required."
            )
        try:
            to_user = User.objects.get(email=to_user_identifier)
        except User.DoesNotExist:
            try:
                to_user = User.objects.get(username=to_user_identifier)
            except User.DoesNotExist:
                raise serializers.ValidationError("User not found.")
        if from_user == to_user:
            raise serializers.ValidationError(
                "You can't send a friend request to yourself."
            )
        existing_request = FriendRequest.objects.filter(
            from_user=from_user,
            to_user=to_user,
        ).first()

        if existing_request:
            raise serializers.ValidationError(
                "A friend request already exists between these users. Current status : "
                + existing_request.status
            )
        data["to_user"] = to_user
        return data

    def create(self, validated_data):
        return super().create(validated_data)


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "username"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"})


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username"]


class FriendRequestDataSerializer(serializers.ModelSerializer):
    from_user = UserSerializer()
    to_user = UserSerializer()

    class Meta:
        model = FriendRequest
        fields = "__all__"
