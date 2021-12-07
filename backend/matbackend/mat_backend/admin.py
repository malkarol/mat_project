from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
import mat_backend.models as m
# Register your models here.

class CustomUser(UserAdmin):
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('Fullname', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions', 'UserType'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('PricingPlan', 'MLBackground')
        })
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('Fullname', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions', 'UserType'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('PricingPlan', 'MLBackground')
        })
    )

admin.site.register(m.User, CustomUser)
admin.site.register(m.Participant)
admin.site.register(m.MLModel)
admin.site.register(m.SessionResult)
admin.site.register(m.Session)