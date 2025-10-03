from django.contrib import admin
from .models import UserProfile
from groups_module.models import Group, GroupMembership


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_superuser')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'supervisor')
    search_fields = ('name',)
    list_filter = ('supervisor',)


@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'group', 'role', 'is_active', 'joined_at')
    list_filter = ('role', 'is_active', 'joined_at')
    search_fields = ('user__email', 'group__name')
    autocomplete_fields = ['user', 'group']
    list_editable = ('role', 'is_active')
