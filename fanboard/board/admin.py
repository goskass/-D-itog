from django.contrib import admin
from .models import RegistrationConfirmation, Ad, Response


class AdAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'text', 'category', 'created_at' ]

admin.site.register(Ad, AdAdmin)

class RegistrationConfirmationAdmin(admin.ModelAdmin):
    list_display = ['user', 'confirmation_code', 'created_at', 'is_confirmed']

class ResponseAdmin(admin.ModelAdmin):
    list_display = ['ad', 'user', 'text', 'created_at', 'is_approved']



admin.site.register(RegistrationConfirmation, RegistrationConfirmationAdmin)
admin.site.register(Response, ResponseAdmin)

