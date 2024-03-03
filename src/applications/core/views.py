from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework import status, viewsets
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from core.serializers import UserAuthSerializer, UserDetailSerializer, UserCSVSerializer
from .models import User
from core.utils import create_users_from_csv_parallel
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.db import models
from django.http import HttpResponse
from django.core import serializers 


"""
Basic Authentication
"""
class UserRegistrationView(CreateAPIView):
    serializer_class = UserAuthSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        user = User.objects.filter(username=request.data['username'])
        if user.exists():
            user = authenticate(username=request.data['username'], password=request.data['password'])
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_403_FORBIDDEN)
        else:
            user = User.objects.create(username=request.data['username'], password=make_password(request.data['password']))
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})

class UserLoginView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class UserView(RetrieveAPIView, APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(data={"data": {"results": [serializer.data]}, "error_message": None, "error_type": None}, status=status.HTTP_200_OK)
    
    def get_object(self):
        return self.request.user

  
"""
CSV File Upload
"""
class UserCSVUploadAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserCSVSerializer

    def post(self, request):
        serializer = UserCSVSerializer(data=request.data)
        if serializer.is_valid():
            csv_file = serializer.validated_data['csv_file']

            results = create_users_from_csv_parallel(csv_file)

            response_data = {
                'message': 'Users created successfully.',
                'users': results,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

def UserFilter(request):
    search_term = request.GET.get('q')

    data = User.objects.annotate(
            full_name_address=Concat(F('first_name'), Value(' '), F('last_name'), Value(' '), F('address'), output_field=models.TextField())
        ).annotate(
            search=SearchVector('first_name', 'last_name', 'address')
        ).annotate(
            rank=SearchRank('search', SearchQuery(search_term))
    ).filter(search=SearchQuery(search_term)).order_by('-rank', 'date_of_birth')

    data = serializers.serialize('json', data, fields=('first_name', 'last_name', 'address')) 

    return HttpResponse(data, content_type="application/json")