from .models import Chat

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
#from django.contrib.auth.models import User


# @receiver(post_save, sender=Chat)
# def post_save_members_count(sender, instance, created, *args, **kwargs):
#     if created:
#         #instance.users.add(instance.admin.id)
#         instance.members_count = instance.users.all().count()+1
#         instance.save()


@receiver(m2m_changed, sender=Chat.users.through)
def m2m_changed_update_members_count(sender, instance, action, *args, **kwargs):
    #instance.users.add(instance.admin.id)
    if action == "post_add":
        instance.members_count = instance.users.all().count()+1
        #instance.users.add(instance.admin.id)
        instance.save()