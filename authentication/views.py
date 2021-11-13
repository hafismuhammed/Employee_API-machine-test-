from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from .utils import get_tokens


class LoginAPIView(APIView):
    def post(self, request, **kwargs):
        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                data = {
                    'message': 'Login Success',
                    'username': user.username,
                    'email': user.email,
                    'tokens': get_tokens(user)
                }
                return Response(data, status=status.HTTP_200_OK)
            error = {'message': 'Account not active'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        else:    
            error = {'status': 'Incorrect user credentials'}
            return Response(error, status=status.HTTP_401_UNAUTHORIZED)
