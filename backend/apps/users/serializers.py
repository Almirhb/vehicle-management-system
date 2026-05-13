from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "role",
            "national_id",
            "phone",
            "email_verified",
            "is_active",
            "is_staff",
            "is_superuser",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "email_verified",
            "is_active",
            "is_staff",
            "is_superuser",
            "created_at",
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "role",
            "national_id",
            "phone",
            "email_verified",
            "is_active",
            "is_staff",
            "is_superuser",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "email_verified",
            "is_active",
            "is_staff",
            "is_superuser",
            "created_at",
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "role",
            "national_id",
            "phone",
        ]
        read_only_fields = ["id"]

    def validate_email(self, value):
        if value:
            value = value.strip().lower()
            if User.objects.filter(email__iexact=value).exists():
                raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_username(self, value):
        value = value.strip()
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)

        if not validated_data.get("role"):
            user.role = "user"

        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "role",
            "national_id",
            "phone",
            "email_verified",
            "is_active",
            "is_staff",
            "is_superuser",
        ]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        user = self.context["request"].user
        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError({"old_password": "Old password is incorrect."})
        return attrs

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save(update_fields=["password"])
        return user


UserSerializer = UserListSerializer