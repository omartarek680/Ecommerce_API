from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate

User = get_user_model()




class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        validators=[validate_password]
    )

    phone = serializers.CharField(
        required=True,
        max_length=15,
        min_length=11
    )

    first_name = serializers.CharField(
        required=True,
        max_length=50,
        min_length=3
    )

    last_name = serializers.CharField(
        required=True,
        max_length=50,
        min_length=3
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone",
            "created_at"
        )

        read_only_fields = ("id", "created_at")

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        return user
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data["confirm_password"] != data["new_password"]:
            raise serializers.ValidationError("Password fields didn't match.")

        return data
    
    def validate_old_password(self, value):
        user = self.context.get("request").user
        if not user.check_password(value):
            raise serializers.ValidationError("Old Password Is Not Correct")

        return value
    