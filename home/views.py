from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from home import models
# Create your views here.


# return HttpResponse("HttpResponse : /home/templates/welcome_home.html.")


# return HttpResponse("HttpResponse : /home/templates/home.html.")
def main_home(request):
    return render(request, 'main_home.html')


@method_decorator(csrf_exempt, name='dispatch')
def search(request):
    if (request.method == 'POST'):
        data = json.loads(request.body)
        category = data["search_category"]
        keyword = data["food_keyword"]

        res = models.food_search(category, keyword)
        if not res:
            return JsonResponse({'message': 'DB_ERR'}, status=400)
        else:
            return JsonResponse({'message': 'SUCCESS', 'result': res}, status=200)


def