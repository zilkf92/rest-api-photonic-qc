from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings


class RequestData(models.Model):
    """This is the model for the data structure that is expected from request"""
    data = models.TextField()
    access_token = models.CharField(max_length=255)
    shots = models.PositiveIntegerField()
    no_qubits = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    is_fetched = models.BooleanField(default=False)
    result = models.TextField(default="")


class UserProfileManager(BaseUserManager):
    """
    Manager for user profiles with BaseUserManager as parent class
    Manipulates objects within the model that the manager is for
    """

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        # Case when email is either empty string or null value
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
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
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    # Determines access to Django admin etc
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    # Normally called username; USERNAME_FIELD required by default
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of our user"""
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
        on_delete=models.CASCADE
    )
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the model as a string"""
        return self.status_text
