from rest_framework import serializers
from .models import User, Asset, Request
from rest_framework.serializers import ModelSerializer, SerializerMethodField
import cloudinary
from cloudinary import config
# User Serializer
class UserSerializer(ModelSerializer):
    profile_picture_url = SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id", "first_name", "last_name", "email", "phone_number", "department", "role", 
            "profile_picture", "profile_picture_url", "created_at", "updated_at", "password"
        ]
        extra_kwargs = {
            "password": {
                "write_only": True,
                "required": True  
            },
        }

    def get_profile_picture_url(self, obj):
        if obj.profile_picture:
            return f"https://res.cloudinary.com/{cloudinary.config().cloud_name}/{obj.profile_picture}"
        return None

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create_user(**validated_data)
        if password:
            user.set_password(password)  # Hash the password
            user.save()
        return user
# Asset Serializer
class AssetSerializer(ModelSerializer):
    image_url = SerializerMethodField()

    class Meta:
        model = Asset
        fields = [
            "id",
            "image",
            "image_url",
            "name",
            "owner",
            "description",
            "category",
            "serial_number",
            "tag",
            "link",
            "status",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        asset = Asset.objects.create(**validated_data)
        return asset


    def get_image_url(self,obj):
        if obj.image:
            return f"https://res.cloudinary.com/{cloudinary.config().cloud_name}/{obj.image}"
        return None
# Request Serializer
class RequestSerializer(ModelSerializer):
    asset = AssetSerializer()
    employee = UserSerializer()

    class Meta:
        model = Request
        fields = [
            "id",
            "asset",
            "employee",
            "status",
            "return_status",
            "notes",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        asset_data = validated_data.pop("asset")
        employee_data = validated_data.pop("employee")

        asset = Asset.objects.create(**asset_data)
        employee = User.objects.create(**employee_data)

        request = Request.objects.create(asset=asset, employee=employee, **validated_data)
        return request