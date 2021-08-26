from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.ChatsList.as_view(), name = 'chatslist'),
    path('add-chat/', views.ChatCreate.as_view(), name = 'add_chat'),
    path('chat/<str:code>/', views.ChatData.as_view(), name = 'chat'),
    path('chat/<str:code>/load-messages/', views.ChatMessagesLoad.as_view(), name = 'load-data'),
    path('chat/<str:code>/load-more-messages/', views.DynamicMessageLoad.as_view(), name = 'more_messages'),
    # path('profiles/<int:id>/', views.Profile.as_view(), name = 'profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
