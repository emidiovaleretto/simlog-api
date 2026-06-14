from django.contrib.auth.models import User
from django.templatetags.static import static
from rest_framework import serializers

from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("simbrief_pilot_id", "picture_profile")

    picture_profile = serializers.SerializerMethodField()

    def get_picture_profile(self, obj):
        request = self.context.get("request")
        placeholder = static("images/placeholder.jpg")
        if obj.picture_profile:
            return request.build_absolute_uri(obj.picture_profile.url) if request else obj.picture_profile.url
        return request.build_absolute_uri(placeholder) if request else placeholder


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )

        return user


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ("id", "username", "email", "profile")

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})
        instance.email = validated_data.get("email", instance.email)
        instance.save()

        profile = instance.profile
        profile.simbrief_pilot_id = profile_data.get("simbrief_pilot_id", profile.simbrief_pilot_id)
        profile.save()

        return instance
