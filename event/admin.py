from django.contrib import admin
from .models import Event, EventInvite

# Register your models here.
admin.site.register(Event)
admin.site.register(EventInvite)