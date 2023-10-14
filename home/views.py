import os

from django.shortcuts import render
from django.http import JsonResponse
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from home import models


# Create your views here.


# return HttpResponse("HttpResponse : /home/templates/welcome_home.html.")


# return HttpResponse("HttpResponse : /home/templates/home.html.")
def main_home(request):
    return render(request, 'home.html')


@method_decorator(csrf_exempt, name='dispatch')
def dbSearch(request):
    if (request.method == 'POST'):
        data = json.loads(request.body)
        category = data["search_category"]
        keyword = data["food_keyword"]

        res = models.food_search(category, keyword)
        if not res:
            return JsonResponse({'message': 'DB_ERR'}, status=400)
        else:
            return JsonResponse({'message': 'SUCCESS', 'result': res}, status=200)
    else:
        return JsonResponse({'message': 'INVALID_HTTP_METHOD'}, status=400)


def rcpHandler(url):
    response = requests.get(url)
    if response.status_code != 200:
        return JsonResponse({'message': 'API_ERR'}, status=400)
    res = json.loads(response.text)
    rcp = res['COOKRCP01']
    return rcp


@method_decorator(csrf_exempt, name='dispatch')
def apiSearch(request):
    if (request.method == 'GET'):
        recipe_name = request.GET.get('keyword')
        url = os.getenv('FOOD_URL') + recipe_name

        rcp = rcpHandler(url)
        result = rcp['RESULT']
        msg = result['MSG']
        count = rcp['total_count']
        rcp_row = rcp['row']

        rowsList = []
        for row in rcp_row:
            name = row.get('RCP_NM', None)
            image = row.get('ATT_FILE_NO_MK', None)
            seq = row.get('RCP_SEQ', None)
            rowsList.append({'name': name, 'image': image, 'seq': seq})
            # 음식 명으로만 검색할 경우 여러가지 값이 해당 명이 포함된 다른 음식들도 검색되기 때문에 일련번호(seq)로 레시피와 영양정보를 알아낼 수 있도록 함
        return JsonResponse({'message': msg, 'total_count': count, 'row': rowsList}, status=200)
    else:
        return JsonResponse({'message': 'INVALID_HTTP_METHOD'}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
def foodDetail(request):
    if (request.method == 'GET'):
        recipe_name = request.GET.get('keyword')
        recipe_seq = request.GET.get('seq')
        url = os.getenv('FOOD_URL') + recipe_name

        rcp = rcpHandler(url)
        rcp_row = rcp['row']

        nutritionList = []
        recipeList = []
        for row in rcp_row:
            seq = row.get('RCP_SEQ', None)
            if seq == recipe_seq:
                name = row.get('RCP_NM', None)
                # 일련번호(seq)로 구분
                eng = row.get('INFO_ENG', None)
                car = row.get('INFO_CAR', None)
                pro = row.get('INFO_PRO', None)
                fat = row.get('INFO_FAT', None)
                na = row.get('INFO_NA', None)
                nutritionList.append({'열량': eng, '탄수화물': car, '단백질': pro, '지방': fat, '나트륨': na})

                dtls = row.get('RCP_PARTS_DTLS', None)
                tip = row.get('RCP_NA_TIP', None)
                recipe = {'재료정보': dtls}
                for i in range(1, 21):
                    man = row.get(f'MANUAL{i:02}', None)
                    img = row.get(f'MANUAL_IMG{i:02}', None)
                    if man :
                        recipe[f'만드는법_{i:02}'] = man
                    if img :
                        recipe[f'만드는법_이미지_{i:02}'] = img
                recipe['저감 조리법 TIP'] = tip
                recipeList.append(recipe)

        return JsonResponse({'메뉴명': name, '영양성분': nutritionList, '레시피': recipeList}, status=200)
    else:
        return JsonResponse({'message': 'INVALID_HTTP_METHOD'}, status=400)
