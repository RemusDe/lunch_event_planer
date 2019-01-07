from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

import datetime
import json

from app.models import Order

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def index(request):
    response = json.dumps([{}])
    return HttpResponse(response, content_type='text/json')


def get_order(request, id):
    if request.method == 'GET':
        try:
            order = Order.objects.get(order_id=id)
            response = json.dumps([{'id': order.order_id, 'date': order.order_date, 'title': order.order_title,
                                    'description': order.order_description, 'price': order.order_price}], default=str)
        except Exception as e:
            print(e)
            response = json.dumps([{'Error': 'No order with this id'}])
    return HttpResponse(response, content_type='text/json')


def get_all_orders(request):
    if request.method == 'GET':
        try:
            order = serializers.serialize('json', Order.objects.all(), fields=(
            'order_id', 'order_date', 'order_title', 'order_description', 'order_price'))
            order = json.loads(order)
            data = {'Orders': order}
            response = data
        except Exception as e:
            print(e)
            response = [{'Error': 'No orders'}]
    return JsonResponse(response, safe=False)


@csrf_exempt
def add_order(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        order_date = datetime.datetime.now()
        order_title = payload['order_title']
        order_description = payload['order_description']
        order_price = payload['order_price']
        order = Order(order_date=order_date, order_title=order_title, order_description=order_description,
                      order_price=order_price)
        try:
            order.save()
            response = json.dumps([{'Success': 'Order added successfully!'}])
        except:
            response = json.dumps([{'Error': 'Order could not be added!'}])
    return HttpResponse(response, content_type='text/json')
