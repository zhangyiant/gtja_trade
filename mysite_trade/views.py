from django.shortcuts import render
from django.http import (
    HttpResponse,
    JsonResponse)
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def index(request):
    return HttpResponse("HelloWorld")

@csrf_exempt
def buy(request):
    data = json.loads(request.body.decode("utf-8"))
    print(data)
    return JsonResponse(data)
