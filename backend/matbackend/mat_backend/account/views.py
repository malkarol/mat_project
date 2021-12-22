from django.shortcuts import render
# to allow other domain to access our methods
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.response import Response
from account.models import User
from account.serializers import UserSerializer
from django.contrib.auth import get_user_model
# piece of information about JsonResponse
# The safe boolean parameter defaults to True.
# If it’s set to False, any object can be passed for serialization
# (otherwise only dict instances are allowed).
# If safe is True and a non-dict object is passed as the first argument,
#  a TypeError will be raised.

#@csrf_exempt
@api_view(['GET', 'POST'])
def users_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method =='GET':
        users = User.objects.all()
        users_serializer = UserSerializer(users, many=True)
        return JsonResponse(users_serializer.data,safe=False)
    elif request.method == 'POST':
        users_data = JSONParser().parse(request)
        users_serializer = UserSerializer(data=users_data)
        if users_serializer.is_valid():
            users_serializer.save()
            return JsonResponse("User created successfully", safe=False)
        return JsonResponse("Falied to create new User", safe=False)

@csrf_exempt
def user_details(request,username):
    if request.method =='GET':
        user = User.objects.get(username=username)
        user_serializer = UserSerializer(user)
        return JsonResponse(user_serializer.data,safe=False)

    elif request.method == 'PUT':
        user_data = JSONParser().parse(request)
        # source:
        # https://stackoverflow.com/questions/4659360/get-django-object-id-based-on-model-attribute
        # user = User.objects.get(email=user_data['email'])
        user = User.objects.get(pk=user_data['id'])
        # if we had field Id
        # user = User.objects.get(userId = user_data['Id'])
        users_serializer = UserSerializer(user, data=user_data)
        if users_serializer.is_valid():
            users_serializer.save()
            return JsonResponse("User's data updated successfully", safe=False)
        return JsonResponse("Failed to update user's data")

    elif request.method =='DELETE':
        user_data = JSONParser().parse(request)
        user = User.objects.get(pk=user_data['id'])
        user.delete()
        return JsonResponse("User deleted successfully", safe=False)


