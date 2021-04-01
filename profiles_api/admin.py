from django.contrib import admin

from profiles_api import models

# Tell the Django admin to register our user profile model with the admin site
# And makes it accessible through the admin interface
admin.site.register(models.UserProfile)
admin.site.register(models.ProfileFeedItem)
admin.site.register(models.RequestData)
