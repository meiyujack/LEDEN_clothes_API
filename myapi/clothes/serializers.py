from rest_framework import serializers

from .models import User, Template, Clothes


# class UserSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     username = serializers.CharField(required=True, max_length=9)
#     password = serializers.CharField(required=True, max_length=15)
#     is_superuser = serializers.BooleanField(read_only=True)
#     is_staff = serializers.BooleanField(read_only=True)
#     date_joined = serializers.DateTimeField(read_only=True)
#     is_active = serializers.BooleanField(read_only=True)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "is_superuser",
            "is_staff",
        ]

    def create(self, validated_data):
        u = User.objects.create(username=validated_data["username"])
        u.set_password(validated_data["password"])
        u.save()
        return u

    def update(self, instance, validated_data):
        if "password" in validated_data:
            instance.set_password(validated_data.get("password"))
        # if instance.tel != validated_data.get("tel"):
        #     instance.tel = validated_data["tel"]
        instance.save()
        return instance


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = [
            "id",
            "name",
            "body",
            "users",
        ]

    def create(self, validated_data):
        u = Template.objects.create(name=validated_data["name"], body=validated_data["body"])
        u.users.set(validated_data["users"])
        u.save()
        return u

    def update(self, instance, validated_data):
        if "name" in validated_data:
            instance.name = validated_data["name"]
        if "body" in validated_data:
            instance.body = validated_data["body"]
        if "users" in validated_data:
            instance.users.set(validated_data["users"])
        instance.save()
        return instance
    
    def delete(self, instance):
        instance.delete()
        return instance
    
class ClothesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clothes
        fields = [
            "id",
            "name",
            "color",
            "size",
            "material",
            "type",
        ]

    def create(self, validated_data):
        c = Clothes.objects.create(name=validated_data["name"], color=validated_data["color"], size=validated_data["size"], material=validated_data["material"], type=validated_data["type"])
        c.save()
        return c

    def update(self, instance, validated_data):
        if "name" in validated_data:
            instance.name = validated_data["name"]
        if "color" in validated_data:
            instance.color = validated_data["color"]
        if "size" in validated_data:
            instance.size = validated_data["size"]
        if "material" in validated_data:
            instance.material = validated_data["material"]
        if "type" in validated_data:
            instance.user = validated_data["type"]
        instance.save()
        return instance
