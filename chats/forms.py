from django.forms import ModelForm
from django import forms
from .models import Chat, Message


class ChatAddForm(ModelForm):
    class Meta:
        model = Chat
        fields = ['name', 'users']

    def __init__(self, *args, **kwargs):
        super(ChatAddForm, self).__init__(*args, **kwargs)
        #self.fields['name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        #self.fields['creator'].widget = forms.TextInput(attrs={'class': 'form-control'})


class AddMessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['message']

    # def __init__(self, *args, **kwargs):
    #     super(AddMessageForm, self).__init__(*args, **kwargs)
    #     self.fields['message'].widget = forms.TextInput(attrs={'class': 'form-control'})