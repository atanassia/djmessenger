#from django.contrib.auth.models import User
#from django.conf import settings


from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic import CreateView, DetailView

from .forms import ChatAddForm, AddMessageForm
from .models import Chat, Message

from django.http import JsonResponse
#from django.core.serializers import serialize

from django.db.models import Q
from django.contrib.auth import get_user_model
User = get_user_model()

def json(request):
    chats = Chat.objects.all()
    chat_serialized_data = []
    for chat in chats:
        chat_serialized_data.append({
            'chatname': chat.name,
            'admin': chat.admin.username,
            'members_count': chat.members_count,
        })

    # chat_serialized_data = serialize('python', chats)
    context = {
        'chat':chat_serialized_data,
    }
    return JsonResponse(context)


class ChatsList(ListView):
    model = Chat
    template_name = 'chats/chats_list.html'
    paginate_by = 10
    context_object_name = 'chats'
    #queryset = Chat.objects.all()


class ChatCreate(CreateView):
    form_class = ChatAddForm
    template_name = 'chats/add_chat.html'


class ChatDetails(View):

    def get(self, request, code, *args, **kwargs):
        choosen_chat = Chat.objects.get(code = code)
        messages = Message.objects.filter(chat = choosen_chat)
        context = {'messages':messages, 'chat':choosen_chat}
        return render(request, 'chats/chat_detail.html', context)
    

    def post(self, request, code, *args, **kwargs):
        choosen_chat = Chat.objects.get(code = code)
        form = AddMessageForm(request.POST)
        add_message = form.save(commit = False)
        if request.user.is_authenticated:
            add_message.sender = request.user
        else:
            add_message.sender = User.objects.get(id = 1)
        add_message.chat = choosen_chat
        form.save()
        messages = Message.objects.filter(chat = choosen_chat)
        context = {'messages':messages, 'chat':choosen_chat}
        return render(request, 'chats/chat_detail.html', context)


class DynamicMessagesLoad(View):
    
    @staticmethod
    def get(request, code, *args, **kwargs):
        choosen_chat = Chat.objects.get(code = code)
        last_message_id = request.GET.get('lastMessageId')
        print(last_message_id)
        more_messages = Message.objects.filter(Q(chat = choosen_chat) & Q(pk__gt = int(last_message_id))).values('id', 'sender', 'message', 'is_readed', 'created')
        if not more_messages:
            return JsonResponse({'data':False})
        data = []
        for message in more_messages:
            obj ={
                'id':message['id'],
                'sender':message['sender'],
                'message':message['message'],
                'is_readed':message['is_readed'],
                'created':message['created']
            }
            data.append(obj)
        data[-1]['last_post'] = True
        return JsonResponse({'data':data})



class Profile(DetailView):
    model = User
    pk_url_kwarg = 'id'
    context_object_name = 'user'
    template_name = 'chats/profile.html'