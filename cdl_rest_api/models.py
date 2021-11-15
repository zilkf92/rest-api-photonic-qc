# Import standard base classes that are needed to use when overwriting or
# customizing the default Django user model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


class QubitMeasurementItem(models.Model):
    """
    This model represents the Qubit Measurement Settings according to
    projection in complex plane
    """

    encodedQubitIndex = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
        ]
    )
    theta = models.DecimalField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(360),
        ],
        decimal_places=2,
        max_digits=5,
    )
    phi = models.DecimalField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(360),
        ],
        decimal_places=2,
        max_digits=5,
    )
    ComputeSettings = models.ForeignKey(
        "ComputeSettings",
        on_delete=models.SET_NULL,  # hatten hier CASCADE?
        null=True,
        related_name="encodedQubitMeasurements",
    )


class CircuitConfigurationItem(models.Model):
    """
    This model contains the name and value of the abstract circuit angles
    """

    circuitAngleName = models.CharField(max_length=255)
    circuitAngleValue = models.DecimalField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(360),
        ],
        decimal_places=3,
        max_digits=6,
    )
    qubitComputing = models.ForeignKey(
        "qubitComputing",
        on_delete=models.SET_NULL,
        null=True,
        related_name="circuitAngles",
    )


class clusterState(models.Model):
    """ """

    numberOfQubits = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(4),
        ]
    )
    graphState = models.CharField(max_length=255)


class qubitComputing(models.Model):
    """ """

    # qubitComputing has 1 field and 1 array
    # array is handled in serializer
    circuitConfiguration = models.CharField(max_length=255)


class ComputeSettings(models.Model):
    """ """

    clusterState = models.ForeignKey(
        "clusterState",
        on_delete=models.SET_NULL,
        null=True,
    )
    qubitComputing = models.ForeignKey(
        "qubitComputing",
        on_delete=models.SET_NULL,
        null=True,
    )


class ExperimentBase(models.Model):
    """ """

    experimentName = models.CharField(max_length=255)
    projectId = models.CharField(max_length=255)
    maxRuntime = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(120),
        ]
    )
    ComputeSettings = models.ForeignKey(
        "ComputeSettings",
        on_delete=models.SET_NULL,
        null=True,
    )


class Experiment(ExperimentBase):
    """ """

    experimentId = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    # a user can have multiple Experiments
    # currently only implemented in Experiment and not in Results
    # as Result is assigned to Experiment (can be changed later to
    # assign to user)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )


class ExperimentResult(models.Model):
    """ """

    startTime = models.DateTimeField(auto_now_add=True)
    totalCounts = models.PositiveIntegerField()
    numberOfDetectors = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(8),
        ]
    )
    singlePhotonRate = models.DecimalField(
        decimal_places=2,
        max_digits=8,
    )
    totalTime = models.PositiveIntegerField()
    experiment = models.ForeignKey(
        "Experiment",
        on_delete=models.SET_NULL,
        null=True,
    )


class Job(models.Model):
    """
    This is the model for the Job data structure that is sent to the Backend
    """

    access_token = models.CharField(max_length=255)  # one time token
    shots = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(200),
        ]
    )
    no_qubits = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(6),
        ]
    )
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )
    is_fetched = models.BooleanField(default=False)


class Result(models.Model):
    """
    This is the model for the Result data structure that is sent from the BE
    """

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        null=True,
    )
    results = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )


class SingleQubitGate(models.Model):
    """
    This model represents the operation on a single qubit and is involved as
    a list of dictionaries in the "experiment" field in Job model.
    Example use {
    {"name": "HWP or QWP", "qubits": "[0]", "params": 22.5},
    {"name": "measure", "qubits": "[0]", "params": 5}
    }
    """

    name = models.TextField()
    qubits = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(7),
        ]
    )
    params = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True)


# User Manager class tells Django how to work with the customized
# user model in CLI. By default when a user is created it expects
# a username and a password field but the username field has been
# replaceed with an email field so a custom User Manager is needed.
class UserProfileManager(BaseUserManager):
    """
    Manager for user profiles with BaseUserManager as parent class.
    Functions within this class are used to manipulate objects
    within the model that the manager is for.
    """

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        # Case when email is either empty string or null value
        # Raise exception
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        # By default self.model is set to the model that the manager is for
        user = self.model(email=email, name=name)

        # Use set_password function that comes with user model
        # Makes sure the password is stored as hash in database
        user.set_password(password)
        # Standard procedure for saving objects in Django
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        # Self is automatically passed in for any class functions
        # When it is called from a different function or a different part
        user = self.create_user(email, name, password)

        # is_superuser is automatically created by PermissionsMixin
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for user in the system"""

    # Define various fields that model should provide
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    # Determines fields for the permission system
    is_active = models.BooleanField(default=True)
    # Determines acces to Django admin
    is_staff = models.BooleanField(default=False)
    # Specify model manager
    # This is required because the custom user model is used with
    # the Django CLI
    objects = UserProfileManager()

    # Overwriting the default USERNAME_FIELD which is normally user name
    # and replacing it with email field
    # When users authenticate they provide email address and pw
    USERNAME_FIELD = "email"
    # Adding username to additional REQUIRED_FIELDS
    REQUIRED_FIELDS = ["name"]

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    # Converting a user profile object into a string
    def __str__(self):
        """Return string representation of our user"""
        # String representation is email address
        return self.email


class ProfileFeedItem(models.Model):
    """Profile status update"""

    # Link models to other models in Django with ForeignKey
    # Here: can never create a ProfileFeedItem for a
    # user profile that doesn't exist
    user_profile = models.ForeignKey(
        # Could also be specified as string
        settings.AUTH_USER_MODEL,
        # Specify what happens to ProfileFeedItem when user
        # profile is deleted
        on_delete=models.CASCADE,
    )
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the model as a string"""
        return self.status_text
