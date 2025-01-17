from django.shortcuts import render
from .serializers import UserRegistrationSerializer,BlogSerializer,UpdateUserSerializer
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.permissions import IsAuthenticated 
from rest_framework.decorators import api_view ,permission_classes
from rest_framework.pagination import PageNumberPagination
from .models import Blog,CustomUser


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
def update_user_detail(request):
    user=request.user
    serializer=UpdateUserSerializer(user,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def update_user_detail(request):
#     user = request.user
#     serializer = UpdateUserSerializer(user, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    
    
class BlogListPagination(PageNumberPagination):
    page_size=6
    





@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_blog(request):
    user=request.user
    serializers=BlogSerializer(data=request.data)
    if serializers.is_valid():
        serializers.save(author=user)
        return Response( serializers.data)
    return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

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
        return Response({"Error":"You can edit blog"})
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
    
  
    
    