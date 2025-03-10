from django.shortcuts import render
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer,BlogSerializer,UpdateUserSerializer,UserInfoSerializer
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.permissions import IsAuthenticated 
from rest_framework.decorators import api_view ,permission_classes
from rest_framework.pagination import PageNumberPagination
from .models import Blog,CustomUser


class BlogListPagination(PageNumberPagination):
    page_size=4


# Create your views here.
@api_view(["POST"])
def register_user(request):
    serializer=UserRegistrationSerializer( data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    user=request.user
    serializer=UpdateUserSerializer(user,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def update_user_profile(request):
#     user = request.user
#     serializer = UpdateUserProfileSerializer(user, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    





@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_blog(request):
    user=request.user
    serializer=BlogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=user)
        return Response( serializer.data)
    else:
        print (serializer.errors)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# BEFORE ADD PAGINATION
# @api_view(['GET'])
# def list_blog(request):
#     blogs=Blog.objects.all()
#     serializer=BlogSerializer(blogs,many=True)
#     return Response(serializer.data)


@api_view(['GET'])
def list_blog(request):
    blogs=Blog.objects.all()
    # FOR PAGINATION
    paginator=BlogListPagination()
    paginated_blogs=paginator.paginate_queryset(blogs,request)
    
    serializer=BlogSerializer(paginated_blogs,many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['PUT'])   
@permission_classes([IsAuthenticated])
def update_blog(request,pk):
    user=request.user
    blog=Blog.objects.get(id=pk)
    if blog.author !=user:
        return Response({"Error":"You can  not edit blog"})
    serializer=BlogSerializer(blog,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])   
@permission_classes([IsAuthenticated])    
def delete_blog(request,pk):
    user=request.user
    blog=Blog.objects.get(id=pk)
    if blog.author != user:
        return Response({"Error":"unauthorized"},status=status.HTTP_403_FORBIDDEN)
    blog.delete()
    return Response({"message":"Succefully Deleted"},status=status.HTTP_204_NO_CONTENT)
    
  
    
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_blogs(request,slug):
    blog=Blog.objects.get(slug=slug)
    serializer=BlogSerializer(blog)
    return Response(serializer.data)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_username(request):
    user=request.user
    username=user.username
    return Response({"username":username})  

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request, username):
    User=get_user_model()
    user=User.objects.get(username=username)
    serializer=UserInfoSerializer(user)
    return Response(serializer.data)
    
      
 
    
    