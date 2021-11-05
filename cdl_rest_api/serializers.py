from rest_framework import serializers

from cdl_rest_api import models


class QubitMeasurementItemSerializer(serializers.ModelSerializer):
    """ """

    class Meta:
        model = models.QubitMeasurementItem
        fields = "__all__"


class CircuitConfigurationItemSerializer(serializers.ModelSerializer):
    """ """

    class Meta:
        model = models.CircuitConfigurationItem
        fields = "__all__"


class clusterStateSerializer(serializers.ModelSerializer):
    """ """

    choices = ["linear", "ghz"]
    graphState = serializers.ChoiceField(choices)

    class Meta:
        model = models.clusterState
        fields = "__all__"


class qubitComputingSerializer(serializers.Serializer):
    """ """

    # To Do: Cluster state configurations need to be added here
    choices = [
        "horseshoe",
    ]
    circuitConfiguration = serializers.ChoiceField(choices)
    # assigns array of CircuitConfigurationItems for GET
    circuitAngles = CircuitConfigurationItemSerializer(many=True)

    def create(self, validated_data):
        """ """
        # remove circuitAngles array from validated_data and store it in
        # circuitAnglesData
        circuitAnglesData = validated_data.pop("circuitAngles")
        # create qubitComputing database entry
        qubitComputing = models.qubitComputing.objects.create(**validated_data)
        # for each pair of Angle + Value, create CircuitConfigurationItem with
        # ForeignKey = qubitComputing that has been created
        for circuitAngle in circuitAnglesData:
            models.CircuitConfigurationItem.objects.create(
                # ** interchanges a dict to a tuple
                qubitComputing=qubitComputing,
                **circuitAngle
            )
        return qubitComputing


class ComputeSettingsSerializer(serializers.ModelSerializer):
    """ """

    encodedQubitMeasurements = QubitMeasurementItemSerializer(many=True)

    def create(self, validated_data):
        """ """
        encodedQubitMeasurementsData = validated_data.pop("encodedQubitMeasurements")
        ComputeSettings = models.ComputeSettings.objects.create(**validated_data)
        for encodedQubitMeasurement in encodedQubitMeasurementsData:
            models.QubitMeasurementItem.objects.create(
                ComputeSettings=ComputeSettings, **encodedQubitMeasurement
            )
        return ComputeSettings

    class Meta:
        model = models.ComputeSettings
        fields = "__all__"
        # return entire object of ForeignKey assignment not just id
        depth = 1


# To Do: Serializer fertigstellen
class ExperimentSerializer(serializers.ModelSerializer):
    """ """

    choices = ["RUNNING", "FAILED", "DONE"]
    status = serializers.ChoiceField(choices)

    class Meta:
        model = models.Experiment
        fields = "__all__"
        depth = 1


class ExperimentResultSerializer(serializers.ModelSerializer):
    """ """

    # check if startTime is readonly
    class Meta:
        model = models.ExperimentResult
        fields = "__all__"


class JobSerializer(serializers.ModelSerializer):
    """Serializes Job object"""

    # Overwrites standard function of ModelSerializer
    # take only name from user.name for ForeignKey
    # make human readable user id
    # Here we use predefined ModelSerializer, and overwrite
    # user field of Job model
    user = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = models.Job
        fields = "__all__"


class ResultSerializer(serializers.ModelSerializer):
    """Serializes Result object"""

    user = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = models.Result
        fields = "__all__"


class SingleQubitGateSerializer(serializers.ModelSerializer):
    """ """

    # overwrite job variable with job.id
    job = serializers.ReadOnlyField(source="job.id")
    # define choice fields to validate gate name input
    choices = ["QWP", "HWP", "measure", "reset"]
    name = serializers.ChoiceField(choices)

    class Meta:
        model = models.SingleQubitGate
        # when field is excluded from serializer, serializer ignores
        # the respective field
        # when field is however referred to as null=True in models
        # field can be empty or missing, but serializer checks the field
        fields = "__all__"


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
        fields = ("id", "email", "name", "password")
        # Extra keyword args
        extra_kwargs = {
            "password": {
                # Can only create new or update objects
                # Get request will not include password field in its response
                "write_only": True,
                # Hide input while typing
                "style": {"input_type": "password"},
            }
        }

    # Overwrite the create function and call create_user function
    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data["email"],
            name=validated_data["name"],
            password=validated_data["password"],
        )

        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)

        return super().update(instance, validated_data)


class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serializes profile feed items"""

    class Meta:
        model = models.ProfileFeedItem
        fields = ("id", "user_profile", "status_text", "created_on")
        extra_kwargs = {"user_profile": {"read_only": True}}
