from rest_framework import serializers

from cdl_rest_api import models


class JobSerializer(serializers.ModelSerializer):
    """Serializes Job object"""
    # Overwrites standard function of ModelSerializer
    # take only name from user.name for ForeignKey
    # make human readable user id
    # Here we use predefined ModelSerializer, and overwrite
    # user field of Job model
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = models.Job
        fields = '__all__'


class ResultSerializer(serializers.ModelSerializer):
    """Serializes Result object"""
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = models.Result
        fields = '__all__'


class SingleQubitGateSerializer(serializers.ModelSerializer):
    """ """
    # overwrite job variable with job.id
    job = serializers.ReadOnlyField(source='job.id')
    # define choice fields to validate gate name input
    choices = ["QWP", "HWP", "measure", "reset"]
    name = serializers.ChoiceField(choices)

    class Meta:
        model = models.SingleQubitGate
        # when field is excluded from serializer, serializer ignores
        # the respective field
        # when field is however referred to as null=True in models
        # field can be empty or missing, but serializer checks the field
        fields = '__all__'


# class HelloSerializer(serializers.Serializer):
#     """Serializers a name field for testing our APIView"""
#
#     # Defines expected input for post, put or patch and validates input
#     name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    # ModelSerializer uses Meta class to configure the serializers
    # to point to a specific model
    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        # Extra keyword args
        extra_kwargs = {
            'password': {
                # Can only create new or update objects
                # Get request will not include password field in its response
                'write_only': True,
                # Hide input while typing
                'style': {'input_type': 'password'}
            }
        }

    # Overwrite the create function and call create_user function
    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)


class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serializes profile feed items"""

    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        extra_kwargs = {'user_profile': {'read_only': True}}
