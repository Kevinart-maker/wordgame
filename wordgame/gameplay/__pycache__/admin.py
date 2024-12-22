from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Word, GameContent

# Extending the Django UserAdmin to include custom fields
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'current_level', 'total_score', 'is_staff')
    
    # Specify fields for the user form in admin panel
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('current_level', 'total_score', 'achievements', 'profile_image')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('current_level', 'total_score', 'achievements', 'profile_image')}),
    )

# Registering CustomUser with the extended CustomUserAdmin class
admin.site.register(CustomUser, CustomUserAdmin)

# Registering the Word model for word database management
@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('word', 'definition')  # Make sure 'word' and 'definition' exist in the Word model
    search_fields = ('word',)

# Registering GameContent for content management
@admin.register(GameContent)
class GameContentAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'text')  # Ensure 'content_type' and 'text' exist in the GameContent model
    search_fields = ('content_type',)
