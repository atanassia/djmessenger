from django.contrib import admin

from .models import Chat, ChatMessages, Dialog, DialogMessages


admin.site.register(Chat)
admin.site.register(ChatMessages)
admin.site.register(Dialog)
admin.site.register(DialogMessages)
