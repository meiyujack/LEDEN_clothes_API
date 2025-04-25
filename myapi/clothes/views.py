import json

from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User,Template,Clothes
from .serializers import UserSerializer,TemplateSerializer


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {"message": "Hello, World!"}
        return Response(content)


# class VerifyAuthView(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request, format=None):
#         content = {
#             "user": str(request.user),
#             "auth": str(request.auth),
#         }
#         return Response(content)




def handle_body(request):
    return json.loads(request.body.decode("utf-8"))


def get_user_by_auth(request):
    authorization = request.META.get("HTTP_AUTHORIZATION")
    if authorization:
        auth = authorization.split(" ")[1]
        t = Token.objects.get(pk=auth)
        u = User.objects.get(pk=t.user_id)
        return u
    return None


def headers_auth2json(request) -> UserSerializer:
    u = get_user_by_auth(request)
    if u:
        serializer = UserSerializer(u)
        return serializer
    return None

def dict2text(d:dict)->str:
    result=""
    for k,v in d.items():
        result+=f"{k}={v},"
    return result[:-1]

@api_view(["GET"])
def verify_auth(request):
    serializer = headers_auth2json(request)
    if serializer:
        u = serializer.data
        u.pop("password")
        return Response(u, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def UsersApiOverview(request):
    users_api_urls = {
        "all_users": "users/",
        "search by name": "users/?username=username/",
        "search by is_superuser": "users/?is_superuser=true/",
        "signup": "users/signup/",
        "update": "/users/username",
    }

    return Response(users_api_urls)


@api_view(["POST"])
def signup(request):
    us = UserSerializer(data=request.data)

    if User.objects.filter(**request.data).exists():
        raise serializers.ValidationError("用户已存在")

    if us.is_valid():
        us.save()
        return Response(us.data, status=status.HTTP_201_CREATED)
    else:
        return Response(us.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"details": "需要用户名和密码"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(
            {"details": "无效的用户名或密码"}, status=status.HTTP_400_BAD_REQUEST
        )

    if not user.check_password(password):
        return Response(
            {"details": "无效的用户名或密码"}, status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)
    else:
        return Response({"details": "验证失败"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_user(request):
    u = get_user_by_auth(request)
    if u and u.is_superuser:
        if request.query_params:
            users = User.objects.filter(**request.query_params.dict())

        if users:
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"details": "没有找到用户"}, status=status.HTTP_404_NOT_FOUND
            )
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
def update_user(request, pk):
    if headers_auth2json(request):
        user = User.objects.get(pk=pk)
        us = UserSerializer(instance=user, data=request.data)

        if us.is_valid():
            us.save()
            return Response(us.data)
        else:
            return Response(us.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(["DELETE"])
def delete_user(request, pk):
    su = headers_auth2json(request)
    if su and json.loads(su)["is_superuser"] == True:
        user = get_object_or_404(User, pk=pk)
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def get_template(request):
    su = headers_auth2json(request)
    if su and json.loads(su)["is_superuser"] == True:
        template = Template.objects.all()
        serializer = TemplateSerializer(template, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(["POST"])
def add_template(request):
    su = headers_auth2json(request)
    if su and json.loads(su)["is_superuser"] == True:
        template = TemplateSerializer(data=request.data)
        if template.is_valid():
            template.save()
            return Response(template.data, status=status.HTTP_201_CREATED)
        else:
            return Response(template.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(["PUT"])
def update_template(request, pk):
    su = headers_auth2json(request)
    if su and json.loads(su)["is_superuser"] == True:
        template = get_object_or_404(Template, pk=pk)
        serializer = TemplateSerializer(instance=template, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(["DELETE"])
def delete_template(request, pk):
    su = headers_auth2json(request)
    if su and json.loads(su)["is_superuser"] == True:
        template = get_object_or_404(Template, pk=pk)
        template.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(["GET"])
def get_clothes(request):
    su = headers_auth2json(request)
    if su and json.loads(su)["is_superuser"] == True:
        clothes = Clothes.objects.all()
        serializer = TemplateSerializer(clothes, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(["POST"])
def add_clothes(request):
    su = headers_auth2json(request)
    if su and json.loads(su)["is_superuser"] == True:
        clothes = TemplateSerializer(data=request.data)
        if clothes.is_valid():
            clothes.save()
            return Response(clothes.data, status=status.HTTP_201_CREATED)
        else:
            return Response(clothes.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)