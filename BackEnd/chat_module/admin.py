from django.contrib import admin
from .models import Message, MessageAttachment, MessageReaction, MessageReadStatus

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'room', 'text_preview', 'message_type', 'created_at', 'is_deleted']
    list_filter = ['message_type', 'is_deleted', 'created_at']
    search_fields = ['text', 'user__username', 'room__name']
    readonly_fields = ['created_at', 'updated_at']
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Message'

@admin.register(MessageAttachment)
class MessageAttachmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'message', 'file_name', 'file_size', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['file_name', 'message__text']

@admin.register(MessageReaction)
class MessageReactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'message', 'user', 'reaction_type', 'created_at']
    list_filter = ['reaction_type', 'created_at']
    search_fields = ['user__username', 'message__text']

@admin.register(MessageReadStatus)
class MessageReadStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'message', 'user', 'read_at']
    list_filter = ['read_at']
    search_fields = ['user__username', 'message__text']
