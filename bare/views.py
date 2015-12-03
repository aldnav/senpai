
import json

from django.contrib.auth.models import User
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView

from .models import Client, Notification


class HomePageView(TemplateView):

    template_name = "bare/home.html"

    def get_context_data(self, **kwargs):
        if self.request.user.username != 'smith':
            if 'poke_url' not in kwargs:
                kwargs['poke_url'] = reverse('poke')
        return kwargs


def register_client(request):
    if request.method == 'GET':
        registration_id = request.GET.get('value')
        try:
            Client.objects.get(registration_id=registration_id)
        except Client.DoesNotExist:
            Client.objects.create(owner=request.user,
                                  registration_id=registration_id)
        return HttpResponse(status=200)
    return HttpResponse(status=400)


def poke(request):
    if request.method == 'GET':
        owner = request.user
        Notification.objects.create(
            creator=owner,
            owner=User.objects.get(username='smith'),
            body='{} poked you!'.format(owner))
        # return HttpResponse(status=200)
    return HttpResponseRedirect('/')


def get_notification(request):
    if request.method == 'GET':
        notification_id = request.GET.get('notifID')
        notification = None
        try:
            notification = Notification.objects.get(pk=notification_id)
            print notification
        except Notification.DoesNotExist:
            return HttpResponse(status=400)
        serialized_obj = serializers.serialize('json', [notification])
        return HttpResponse(json.dumps(serialized_obj),
                            content_type='application/json')
    return HttpResponse(status=200)


def unregister_client(request):
    if request.method == 'GET':
        client_id = request.GET.get('clientID')
        Client.objects.get(registration_id=client_id).delete()
        return HttpResponse(status=200)
