from django.contrib import admin

# Register your models here.
from .models import User, Agent, Lead, UserProfile, Category


admin.site.register(Category)
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Agent)
admin.site.register(Lead)