from django.contrib import admin

from users.models import User, Address, Area

admin.site.register(User)
admin.site.register(Address)
admin.site.register(Area)
