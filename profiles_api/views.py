from rest_framework.views import APIView
from rest_framework.response import Response # Standard Response object
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions


class JobView(APIView):
    """
    Implements get and post for Job model
    """
    permission_classes = (IsAuthenticated,)
    serializers_class = serializers.JobSerializer

    def get(self, request, pk=None):
        if pk is not None:
            job = None
            if request.user.is_staff:
                if models.Job.objects.filter(pk=pk).exists():
                    job = models.Job.objects.get(pk=pk)
                    if request.data.get('fetch'):
                        job.is_fetched = True
                        job.save()
            else:
                if models.Job.objects.filter(pk=pk, user=request.user).exists():
                    job = models.Job.objects.get(pk=pk, user=request.user)
            if job is not None:
                serializer = self.serializers_class(job)
                return Response(serializer.data)
            else:
                return Response('Job does not exist.')
        else:
            if request.user.is_staff:
                if request.data.get('filtered'):
                    jobs = models.Job.objects.filter(is_fetched=False)
                else:
                    jobs = models.Job.objects.all()
            else:
                if request.data.get('filtered'):
                    jobs = models.Job.objects.filter(
                        user=request.user,
                        is_fetched=False
                        )
                else:
                    jobs = models.Job.objects.filter(user=request.user)
            serializer = self.serializers_class(jobs, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = self.serializers_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        job = serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResultView(APIView):
    """
    Implements get and post for Job model
    """
    permission_classes = (IsAuthenticated,)


# Hello World API View example
class HelloApiView(APIView):
    """Test API View
    Creates a new class based on API View class from Django rest_framework
    Allows to define application logic for the corresponding endpoint
    Endpoint is assigned to view
    """

    # Configures APIView to have serializer class
    # Serializer tells APIView what data to expect for requests to API
    serializers_class = serializers.HelloSerializer

    # Self is required for all class Functions
    # Request object is passed in by rest_framework
    # Format adds format suffix to the end of the endpoint URL
    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_apiview = [
            'Uses HTTP methods as functions (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over your application logic',
            'Is mapped manually to URLs'
        ]

        # Converts the Response object to JSON
        # Needs to be either a list or a dictionary
        return Response({'message':'Hello!', 'an_apiview': an_apiview})

    def post(self, request):
        """Create a hello message with our name"""
        # data needs to get passed as request.data when a post request ist made
        serializer = self.serializers_class(data=request.data)

        # Validate serializer
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                # Give dictionary of all errors based on the validation rules
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    # HTTP PUT is typically send to specific URL primary key (pk)
    # pk=None as default in case pk should not be supported with a request
    # Commonly PUT is applied to URL with the ID of the object
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
    # that is linked to view set, so this lists a set of objects
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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
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
    permission_classes = (
        # Ensure that users can only update statuses where the user
        # profile is assigned to their user
        permissions.UpdateOwnStatus,
        # Users must be authenticated to perform any request that is
        # not a read request
        IsAuthenticated,
    )

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)
