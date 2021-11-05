from django.db.models.query import QuerySet
from rest_framework.views import APIView
from rest_framework.response import Response  # Standard Response object
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import AllowAny, IsAuthenticated

from cdl_rest_api import serializers
from cdl_rest_api import models
from cdl_rest_api import permissions


class JobView(APIView):
    """
    Implements get and post for Job model
    """

    permission_classes = (IsAuthenticated,)
    serializers_class = serializers.JobSerializer

    def create_responselist(self, jobs):
        """
        Defines response dictionary for visualization of the Job model
        and its single qubit gates.
        """
        responselist = []
        if type(jobs) is QuerySet:
            for job in jobs:
                # query single qubit gates for job.id from db
                # objects.filter is built in by Django
                singlequbitgates = models.SingleQubitGate.objects.filter(job=job.id)
                serializer = serializers.SingleQubitGateSerializer(
                    singlequbitgates, many=True
                )
                # define response dict manually
                response_dict = {
                    "id": job.id,
                    "experiment": serializer.data,
                    "access_token": job.access_token,
                    "shots": job.shots,
                    "no_qubits": job.no_qubits,
                    "date": job.date,
                    "user": str(job.user),
                    "is_fetched": job.is_fetched,
                }
                responselist.append(response_dict)
            return responselist
        else:
            # same procedure as in for loop for single job object
            singlequbitgates = models.SingleQubitGate.objects.filter(job=jobs.id)
            serializer = serializers.SingleQubitGateSerializer(
                singlequbitgates, many=True
            )
            response_dict = {
                "id": jobs.id,
                "experiment": serializer.data,
                "access_token": jobs.access_token,
                "shots": jobs.shots,
                "no_qubits": jobs.no_qubits,
                "date": jobs.date,
                "user": str(jobs.user),
                "is_fetched": jobs.is_fetched,
            }
            return response_dict

    def get(self, request, pk=None):
        if pk is not None:
            job = None
            if request.user.is_staff:
                if models.Job.objects.filter(pk=pk).exists():
                    job = models.Job.objects.get(pk=pk)
                    # if get request contains field "fetch"
                    if request.data.get("fetch"):
                        job.is_fetched = True
                        job.save()
            else:
                if models.Job.objects.filter(pk=pk, user=request.user).exists():
                    job = models.Job.objects.get(pk=pk, user=request.user)
                    # Here are multiple Responses missing
            if job is not None:
                return Response(self.create_responselist(job))
            else:
                return Response("Job does not exist.")
        else:
            if request.user.is_staff:
                if request.data.get("filtered"):
                    jobs = models.Job.objects.filter(is_fetched=False)
                else:
                    jobs = models.Job.objects.all()
            else:
                if request.data.get("filtered"):
                    jobs = models.Job.objects.filter(
                        user=request.user, is_fetched=False
                    )
                else:
                    jobs = models.Job.objects.filter(user=request.user)
            return Response(self.create_responselist(jobs))

    def post(self, request):
        # IF validates whether there is experiment field in request data
        # Alternatively custom serializer needs to be built
        if request.data.get("experiment"):
            # here we need now two serializers as we work with 2 models
            # SingleQubitGate and Job
            sqg_serializer = serializers.SingleQubitGateSerializer(
                data=request.data.get("experiment"),
                many=True,  # "experiment" is a list of objects
            )
            # makes job model
            job_serializer = self.serializers_class(data=request.data)
            # validates data against model and ignores additional
            # "experiment" field with respect to Job model
            job_serializer.is_valid(raise_exception=True)
            sqg_serializer.is_valid(raise_exception=True)
            # save as Job model with user = request.user
            # job serializer validates against Job model, so user must
            # be retrieved from logged in user who sends the request
            job = job_serializer.save(user=request.user)
            # saves list of single qubit gates in db and assigns job
            sqg_serializer.save(job=job)
            return Response(self.create_responselist(job), status=status.HTTP_200_OK)
        else:
            # more detailed error message required
            return Response("Error message: experiment field is required")


class ResultView(APIView):
    """
    Implements get and post for Result model
    """

    permission_classes = (
        IsAuthenticated,
        permissions.IsAdminOrReadOnly,
    )
    serializers_class = serializers.ResultSerializer

    def get(self, request, pk=None):
        if pk is not None:  # if primary key specified
            result = None
            if request.user.is_staff:  # if staff user
                if models.Result.objects.filter(pk=pk).exists():
                    result = models.Result.objects.get(pk=pk)
                    # here else statements are missing
            else:  # if regular user
                if models.Result.objects.filter(pk=pk, user=request.user).exists():
                    result = models.Result.objects.get(pk=pk, user=request.user)
                    # else statement missing
            if result is not None:
                serializer = self.serializers_class(result)
                return Response(serializer.data)
            else:
                return Response("Result does not exist.")
        else:  # if primary key is not specified
            if request.user.is_staff:
                results = models.Result.objects.all()
            else:
                results = models.Result.objects.filter(user=request.user)
            serializer = self.serializers_class(results, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = self.serializers_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        job = models.Job.objects.get(id=request.data.get("job"))
        result = serializer.save(user=job.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ModelViewSet specifically designed for managing models through API
class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""

    serializer_class = serializers.UserProfileSerializer
    # Determine objects in the database which are managed in this view
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        "name",
        "email",
    )


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


# Hello World API View example
# class HelloApiView(APIView):
#     """Test API View
#     Creates a new class based on API View class from Django rest_framework
#     Allows to define application logic for the corresponding endpoint
#     Endpoint is assigned to view
#     """
#
#     # Configures APIView to have serializer class
#     # Serializer tells APIView what data to expect for requests to API
#     serializers_class = serializers.HelloSerializer
#
#     # Self is required for all class Functions
#     # Request object is passed in by rest_framework
#     # Format adds format suffix to the end of the endpoint URL
#     def get(self, request, format=None):
#         """Returns a list of APIView features"""
#         an_apiview = [
#             'Uses HTTP methods as functions (get, post, patch, put, delete)',
#             'Is similar to a traditional Django View',
#             'Gives you the most control over your application logic',
#             'Is mapped manually to URLs'
#         ]
#
#         # Converts the Response object to JSON
#         # Needs to be either a list or a dictionary
#         return Response({'message':'Hello!', 'an_apiview': an_apiview})
#
#     def post(self, request):
#         """Create a hello message with our name"""
#         # data needs to get passed as request.data when a post request ist made
#         serializer = self.serializers_class(data=request.data)
#
#         # Validate serializer
#         if serializer.is_valid():
#             name = serializer.validated_data.get('name')
#             message = f'Hello {name}'
#             return Response({'message': message})
#         else:
#             return Response(
#                 # Give dictionary of all errors based on the validation rules
#                 serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#     # HTTP PUT is typically send to specific URL primary key (pk)
#     # pk=None as default in case pk should not be supported with a request
#     # Commonly PUT is applied to URL with the ID of the object
#     def put(self, request, pk=None):
#         """Handle updating an object"""
#         return Response({'method': 'PUT'})
#
#     def patch(self, request, pk=None):
#         """Handle a partial update of an object"""
#         return Response({'method': 'PATCH'})
#
#     def delete(self, request, pk=None):
#         """Delete an object"""
#         return Response({'method': 'DELETE'})


# class HelloViewSet(viewsets.ViewSet):
#     """Test API ViewSet"""
#     serializers_class = serializers.HelloSerializer
#
#     # list is typically a HTTP GET to the root of the endpoint
#     # that is linked to view set, so this lists a set of objects
#     # that the view set represents
#     def list(self, request):
#         """Return a hello message"""
#
#         a_viewset = [
#             'Uses actions (list, create, retrieve, update, partial_update)',
#             'Automatically maps to URLs using Routers',
#             'Provides more functionality with less code',
#         ]
#
#         return Response({'message': 'Hello!', 'a_viewset': a_viewset})
#
#     def create(self, request):
#         """Create a new hello message"""
#         serializer = self.serializers_class(data=request.data)
#
#         if serializer.is_valid():
#             name = serializer.validated_data.get('name')
#             message =f'Hello {name}!'
#             return Response({'message': message})
#         else:
#             return Response(
#                 serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#     def retrieve(self, request, pk=None):
#         """Handle getting an object by its ID"""
#         return Response({'http_method': 'GET'})
#
#     def update(self, request, pk=None):
#         """Handle updating an object"""
#         return Response({'http_method': 'PUT'})
#
#     def partial_update(self, request, pk=None):
#         """Handle updating part of an object"""
#         return Response({'http_method': 'PATCH'})
#
#     def destroy(self, request, pk=None):
#         """Handle removing an object"""
#         return Response({'http_method': 'DELETE'})
