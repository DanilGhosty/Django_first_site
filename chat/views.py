from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.humanize.templatetags.humanize import naturaltime
from .models import Message
import json

@login_required
def load_messages(request, pk):
    other_user = get_object_or_404(User, pk=pk)
    messages = Message.objects.filter(
        Q(receiver=request.user, sender=other_user)
    )
    messages.update(seen=True)
    messages = messages | Message.objects.filter(
        Q(receiver=other_user, sender=request.user)
    ) 
    context = {
        "other_user": other_user,
        "user_messages": messages,
        "users": User.objects.all()
    }
    return render(request, "chatroom.html", context)

@login_required
def load_messages_ajax(request, pk):
    other_user = get_object_or_404(User, pk=pk)
    messages = Message.objects.filter(seen=False, 
                                      receiver=request.user)
    message_list = []
    print ("Messages:")
    for message in messages:
        message_list.append({"sender": message.sender.username,
                             "message": message.message,
                             "sent": message.sender==request.user,
                             "date_created": naturaltime(message.date_created)})
        message.seen = True
    messages.update(seen=True)
    if request.method =="POST":
        message = json.loads(request.body)["message"]
        print (message)
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
    print(len(message_list))
    print(message_list)
    return JsonResponse(message_list, safe=False)
