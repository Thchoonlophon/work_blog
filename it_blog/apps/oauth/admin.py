from django.contrib import admin
from .models import Ouser


@admin.register(Ouser)
class OuserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'date_joined')
    fieldsets = (
        ('Basic Info', {'fields': (('username', 'email'), ('link',))}),
        ('Copyright Info', {'fields': (('is_active', 'is_staff', 'is_superuser'),
                             'groups', 'user_permissions')}),
        ('Important Date', {'fields': (('last_login', 'date_joined'),)}),
    )
    filter_horizontal = ('groups', 'user_permissions',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email')
