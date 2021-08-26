from django.core.serializers import serialize
from django.http.response import HttpResponse

from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic.base import TemplateView, View
from django.views.generic.list import ListView
from django.views.generic import CreateView, DetailView

from .forms import ChatAddForm, AddMessageForm
from .models import Chat, Message

from django.http import JsonResponse
#from django.core.serializers import serialize

from django.db.models import Q
from django.contrib.auth import get_user_model
User = get_user_model()


class ChatsList(ListView):
    """ Вывод списка всех чатов """

    model = Chat
    template_name = 'chats/chats_list.html'
    context_object_name = 'chats'


class ChatCreate(CreateView):
    """ Создание чата """

    form_class = ChatAddForm
    template_name = 'chats/add_chat.html'


class ChatData(View):
    """ Метод get отвечает за отправку шаблона вместе с общими данными чата,
        Метод post отвечает за отправленные на сервер сообщения."""
    
    @staticmethod
    def get(request, code, *args, **kwargs):
        choosen_chat = Chat.objects.get(code = code)
        context = {'chat':choosen_chat}
        return render(request, 'chats/chat_detail.html', context)

    @staticmethod
    def post(request, code, *args, **kwargs):
        form = AddMessageForm(request.POST)
        choosen_chat = Chat.objects.get(code = code)
        add_message = form.save(commit = False)
        data = {}
        if request.is_ajax():
            if form.is_valid():
                if request.user.is_authenticated:
                    add_message.sender = request.user
                else:
                    add_message.sender = User.objects.get(id = 1)
                add_message.chat = choosen_chat
                form.save()
                data['status'] = 'the message is received'
                return JsonResponse(data)



class ChatMessagesLoad(View):

    """ Ну а тут он просто сообщения запрашивает """
    def post(self, request, code, *args, **kwargs):
        choosen_chat = Chat.objects.get(code = code)
        messages = Message.objects.filter(chat = choosen_chat).values('id', 'sender__username', 'message', 'is_readed', 'created')
        template = render_to_string('chat_components/messages.html', {'messages':messages})
        return HttpResponse(template)


class DynamicMessageLoad(View):
    
    """ Сюда приходят ajax запросы с вопросом 'есть что новое?', если нет-
    отправляю false """
    @staticmethod
    def get(request, code, *args, **kwargs):
        choosen_chat = Chat.objects.get(code = code)
        last_message_id = request.GET.get('lastMessageId')
        if last_message_id == None:
            return JsonResponse({'data':False})
        elif last_message_id == 'begin':
            print('ok begin hi')
            more_messages = Message.objects.filter(chat = choosen_chat).values('id', 'sender__username', 'message', 'is_readed', 'created')
        else:    
            more_messages = Message.objects.filter(Q(chat = choosen_chat) & Q(pk__gt = int(last_message_id))).values('id', 'sender__username', 'message', 'is_readed', 'created')
        if not more_messages:
            return JsonResponse({'data':False})
        data = []
        for message in more_messages:
            obj ={
                'id':message['id'],
                'sender':message['sender__username'],
                'message':message['message'],
                'is_readed':message['is_readed'],
                'created':message['created']
            }
            data.append(obj)
        data[-1]['last_message'] = True
        return JsonResponse({'data':data})