from django.contrib import admin
from . models import UserProfile , Item, Category
from mptt.admin import MPTTModelAdmin


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Item)
admin.site.register(Category, MPTTModelAdmin)