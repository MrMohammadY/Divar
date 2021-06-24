from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'is_active', 'date_joined', 'last_login')
    list_filter = ('is_active', )
    search_fields = ('phone_number',)
