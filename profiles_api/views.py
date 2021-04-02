from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions


class RequestDataViewSet(viewsets.ModelViewSet):
    """ViewSet for RequestData"""
    queryset = models.RequestData.objects.all()
    serializer_class = serializers.RequestDataSerializer
    permission_classes = (permissions.IsOwnerOrAdmin, permissions.AdminViewList,)

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)

    def list(self, request):

        queryset = models.RequestData.objects.filter(is_fetched=False)
        serializer = serializers.RequestDataSerializer(queryset, many=True)

        return Response(serializer.data)

# Hello World API View example
class HelloApiView(APIView):
    """Test API View
    Creates a new class based on API View class from Django rest_framework
    Allows to define application logic for the corresponding endpoint
    Endpoint is assigned to view
    """

    # Configures APIView to have serializer class
    serializers_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_apiview = [
            'Uses HTTP methods as functions (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over your application logic',
            'Is mapped manually to URLs'
        ]

        return Response({'message':'Hello!', 'an_apiview': an_apiview})

    def post(self, request):
        """Create a hello message with our name"""
        serializer = self.serializers_class(data=request.data)

        # Validate serializer
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk=None):
        """Handle updating an object"""
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """Handle a partial update of an object"""
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Delete an object"""
        return Response({'method': 'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    serializers_class = serializers.HelloSerializer

    # list is typically a HTTP GET to the root of the endpoint
    # that is linked to view set, so what this does is list a set of objects
    # that the view set represents
    def list(self, request):
        """Return a hello message"""

        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code',
        ]

        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        """Create a new hello message"""
        serializer = self.serializers_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message =f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""
        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handle updating an object"""
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Handle removing an object"""
        return Response({'http_method': 'DELETE'})

# ModelViewSet specifically designed for managing models through API
class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    # Determine objects in the database which are managed in this view
    queryset = models.UserProfile.objects.all()
    authentication_classes = (SessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)
