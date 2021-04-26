from django.contrib import admin

from profiles_api import models

# Tell the Django admin to register user profile model with the
# admin site and makes it accessible through the admin interface
admin.site.register(models.UserProfile)
admin.site.register(models.ProfileFeedItem)
admin.site.register(models.Job)
admin.site.register(models.Result)

# Django admin sections represent different apps from the project
# Auth token app is automatically added as part of the DRF
# Authentication and authorization is part of django
