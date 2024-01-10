from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import generics
from rest_framework import filters
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.mail import send_mail
from .models import User_Data, BlockedUser
from .serializers import PostSerializer, UserSerializer


class User_Data_ListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Implement filtering by title, body, and author using query parameters
        title = self.request.query_params.get('title', None)
        body = self.request.query_params.get('body', None)
        author = self.request.query_params.get('author', None)

        queryset = User_Data.objects.filter(author=request.user)
        if title:
            queryset = queryset.filter(title__icontains=title)
        if body:
            queryset = queryset.filter(body__icontains=body)
        if author:
            queryset = queryset.filter(author__username=author)

        # Implement pagination
        page = self.request.query_params.get('page', 1)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def user(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)

            # Send email notification using Django signals
            subject = 'New Post Created'
            message = f'Hi {request.user.username}, your post "{serializer.data["title"]}" has been created.'
            from_email = 'your-email@example.com'
            to_email = [request.user.email]
            send_mail(subject, message, from_email, to_email)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class User_Data_DetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        post = generics.get_object_or_404(User_Data, pk=pk, author=request.user)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = generics.get_object_or_404(User_Data, pk=pk, author=request.user)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = generics.get_object_or_404(User_Data, pk=pk, author=request.user)
        # Soft delete (you may implement this based on your model design)
        post.is_deleted = True
        post.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BlockedUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        blocked_users = BlockedUser.objects.filter(user=request.user)
        serializer = UserSerializer(blocked_users, many=True)
        return Response(serializer.data)

    def post(self, request):
        blocked_user_id = request.data.get('blocked_user')
        if blocked_user_id:
            blocked_user = generics.get_object_or_404(User, id=blocked_user_id)
            BlockedUser.objects.create(user=request.user, blocked_user=blocked_user)
            return Response(status=status.HTTP_201_CREATED)
        return Response({'error': 'blocked_user field is required'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        blocked_user_id = request.data.get('blocked_user')
        if blocked_user_id:
            BlockedUser.objects.filter(user=request.user, blocked_user_id=blocked_user_id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'blocked_user field is required'}, status=status.HTTP_400_BAD_REQUEST)