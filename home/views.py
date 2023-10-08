from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.


# return HttpResponse("HttpResponse : /home/templates/welcome_home.html.")
def main_home(request):
    return render(request, 'main_home.html')
