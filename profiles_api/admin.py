from django.contrib import admin

from profiles_api import models

# Tell the Django admin to register user profile model with the
# admin site and makes it accessible through the admin interface
admin.site.register(models.UserProfile)
admin.site.register(models.ProfileFeedItem)
admin.site.register(models.RequestData)
