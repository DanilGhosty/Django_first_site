from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.humanize.templatetags.humanize import naturaltime
from .models import Message
import json

def unread_msg_num(request):
    if request.user.is_authenticated:
        # Get all messages that are unread and are not sent by the current user
        unread_messages = Message.objects.filter(
            Q(seen=False) & Q(sender__is_active=True)
            & Q(receiver__is_active=True) & Q(receiver__id=request.user.id)
        )
        unread_messages_count = unread_messages.count()
        print("UNREAD MESSAGES COUNT: ", unread_messages_count)
        return unread_messages_count

@login_required
def load_mesages_home(request):
    users = None
    if request.method == "POST":
        searched = request.POST.get('searchuser')
        users = User.objects.filter(username__icontains=searched)   
        if users.count()>0:
            return load_messages(request, users[0].pk, users) 
        return load_messages(request, request.user.pk, users)

@login_required
def load_messages(request, pk, users=None):
    other_user = get_object_or_404(User, pk=pk)
    messages = Message.objects.filter(
        Q(receiver=request.user, sender=other_user)
    )
    messages.update(seen=True)
    messages = messages | Message.objects.filter(
        Q(receiver=other_user, sender=request.user)
    ) 
    msg_num = unread_msg_num(request)
    if not users:
        users = User.objects.all() 
    count_msg_users = []   # [(12, user1),(3, user2),()]
    for usr in users:
        msg_count_reseved =  usr.sent_messages.filter(receiver=request.user).count()
        msg_count_sent = usr.received_messages.filter(sender=request.user).count()
        msg_count = msg_count_reseved + msg_count_sent
        count_msg_users.append((msg_count, usr))
    count_msg_users.sort(key=lambda el: el[0],reverse=True)
    users = [usr[1] for usr in count_msg_users]
    context = {
        "other_user": other_user,
        "user_messages": messages,
        "users": users,
        "msg_num": msg_num,
    }
    return render(request, "chatroom.html", context)


def search_user(request):
    return load_mesages_home(request)

@login_required
def load_messages_ajax(request, pk):
    other_user = get_object_or_404(User, pk=pk)
    messages = Message.objects.filter(seen=False, 
                                      receiver=request.user,
                                      sender=other_user)
    message_list = []
    for message in messages:
        message_list.append({"sender": message.sender.username,
                             "message": message.message,
                             "sent": message.sender==request.user,
                             "date_created": naturaltime(message.date_created)})
        message.seen = True
    messages.update(seen=True)
    if request.method =="POST":
        message = json.loads(request.body)["message"]
        if message:
            m = Message.objects.create(
                sender=request.user,
                receiver=other_user,
                message=message
            )
            #m.save()
            message_list.append(
                {"sender": request.user.username,
                "username": request.user.username,
                 "message": m.message,
                 "sent": True,
                 "date_created": naturaltime(m.date_created)}
            )
    return JsonResponse(message_list, safe=False)
