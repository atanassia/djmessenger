from django.contrib import admin
from .models import Chat, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    fieldsets=(
        ('Секция 1', {
            'fields': ('chat', 'sender',),    
        }),

        ('Секция 2', {
            'fields': ('message',),
        }),

        ('Секция 3', {
            'fields': ('is_readed', ('created', 'updated'),),
        }),
    )

    readonly_fields = ['created', 'updated']
    list_display = ('id', 'chat', 'sender','message',)
    list_display_links = ('id', 'chat',)
    list_filter = ('is_readed','updated',)
    search_fields = ('message', 'sender')
    raw_id_fields = ('sender',)


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    fieldsets=(
        ('Секция 1', {
            'fields': (('code','name'),),    
        }),

        ('Секция 2', {
            'fields': ('users',('members_count', 'is_dialog'),),
        }),

        ('Секция 3', {
            'fields': (('created', 'updated'),),
        }),
    )
    readonly_fields = ['code', 'created', 'updated']
    list_display = ('id', 'name', 'members_count',)
    list_display_links = ('id', 'name',)
    list_filter = ('is_dialog','updated',)
    search_fields = ('name', 'code')
    raw_id_fields = ('users',)
    inlines = [MessageInline]
    save_on_top = True