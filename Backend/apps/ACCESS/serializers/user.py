from rest_framework import serializers
from apps.ACCESS.models import User
from rest_framework.authtoken.models import Token
from apps.BASE.serializers import ReadOnlySerializer, WriteOnlySerializer



class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "uuid",
            "identity",
            "phone_number",
            "email",
            "password",
            "confirm_password",
            "token",
            "mode"
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def get_token(self, obj):
        token, _ = Token.objects.get_or_create(user=obj)
        return token.key

    def create(self, validated_data):
        email = validated_data.get("email")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"detail": "User with this email already exists."}
            )

        password = validated_data.get("password")
        confirm_password = validated_data.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError({"error": "Passwords do not match"})

        user = User(
            identity=validated_data.get("identity"),
            email=email,
            phone_number=validated_data.get("phone_number"),
        )
        user.set_password(password)
        user.save()
        return user


    # def get_access_token(self, obj):
    #     """Generate the access token for the user."""
    #     refresh = RefreshToken.for_user(obj)
    #     return str(refresh.access_token)

    # def get_refresh_token(self, obj):
    #     """Generate the refresh token for the user."""
    #     refresh = RefreshToken.for_user(obj)
    #     return str(refresh)


class UserListReadOnlySerializer(ReadOnlySerializer):
    class Meta(ReadOnlySerializer.Meta):
        model = User
        fields = [
            "id",
            "uuid",
            "identity",
            "phone_number",
            "is_active",
            "email",
            "gender",
            "domain",
            "mode"
        ]
class UserListDetailOnlySerializer(ReadOnlySerializer):
    class Meta(ReadOnlySerializer.Meta):
        model = User
        fields = [
            "id",
            "uuid",
            "identity",
            "phone_number",
            "is_active",
            "email",
            "dob",
            "address",
            "city",
            "gender",
            "domain",
            "mode"
        ]



class UserWriteOnlySerializer(WriteOnlySerializer):
    class Meta(WriteOnlySerializer.Meta):
        model = User
        fields = [
            "employee_id",
            "identity",
            "phone_number",
            "is_active",
            "mode"
        ]


class UserDetailSerializer(ReadOnlySerializer):
    
    class Meta(ReadOnlySerializer.Meta):
        model = User
        fields = [
            "id",
            "uuid",
            "employee_id",
            "identity",
            "phone_number",
            "is_active",
        ]


class UserDetailEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "identity",
            "email",
            "phone_number",
            "dob",
            "address",
            "city",
            "gender",
            "domain",
        ]
        extra_kwargs = {
            "email": {"required": False},
            "phone_number": {"required": False},
            "dob": {"required": False},
            "address": {"required": False},
            "city": {"required": False},
            "gender": {"required": False},
            "domain": {"required": False},
        }