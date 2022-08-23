from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    fields = ('id', 'email', 'phone_number', 'date_joined', 'is_superuser')
    list_display = ('email', 'is_superuser')
    search_fields = ('email', 'phone_number', 'is_superuser')
    ordering = ('date_joined',)


admin.site.register(User, UserAdmin)
