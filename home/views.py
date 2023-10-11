import os

from django.shortcuts import render
from django.http import JsonResponse
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.views import View
from home import models


# Create your views here.


# return HttpResponse("HttpResponse : /home/templates/welcome_home.html.")


# return HttpResponse("HttpResponse : /home/templates/home.html.")
def main_home(request):
    return render(request, 'main_home.html')


@method_decorator(csrf_exempt, name='dispatch')
def kakaoLogin(request):
    if (request.method == 'GET'):
        url = os.getenv('KAKAO_URL')
        return JsonResponse({'message': 'SUCCESS', 'result': url}, status=200)
    else:
        return JsonResponse({'message': 'INVALID_HTTP_METHOD'}, status=400)


class KakaoCallbackView(View):
    def get(self, request, *args, **kwargs):
        code = request.GET.get('code', '')

        data = {
            "grant_type": 'authorization_code',
            "client_id": os.getenv('KAKAO_KEY'),
            "redirection_url": os.getenv('REDIRECT_URL'),
            "code": code
        }
        kakao_token_api = "https://kauth.kakao.com/oauth/token"
        access_token = requests.post(kakao_token_api, data=data).json()["access_token"]

        kakao_user_api = "https://kapi.kakao.com/v2/user/me"
        header = {"Authorization": f"Bearer ${access_token}"}
        user_information = requests.get(kakao_user_api, headers=header).json()
        kakao_id = user_information["id"]
        kakao_nickname = user_information["properties"]["nickname"]

        models.saveUserInfo(kakao_id, kakao_nickname)

        return JsonResponse({'message': 'SUCCESS'}, status=200)
        #여기서 success 말고 토큰 발급 구현 필요


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
        return JsonResponse({'message': 'API_ERR'}, status=response.status_code)
    res = json.loads(response.text)
    rcp = res['COOKRCP01']
    return rcp


@method_decorator(csrf_exempt, name='dispatch')
def apiSearch(request):
    if (request.method == 'GET'):
        recipe_name = request.GET.get('keyword')
        if not recipe_name:
            return JsonResponse({'message': 'NO_KEY'}, status=400)
        url = os.getenv('FOOD_URL') + recipe_name

        rcp = rcpHandler(url)
        result = rcp['RESULT']
        msg = result['MSG']

        if rcp['total_count'] == '0':
            return JsonResponse({'message': msg}, status=400)
        else:
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
        if not recipe_name or not recipe_seq:
            return JsonResponse({'message': 'NO_KEY'}, status=400)
        url = os.getenv('FOOD_URL') + recipe_name

        rcp = rcpHandler(url)
        if rcp['total_count'] == '0':
            result = rcp['RESULT']
            return JsonResponse({'message': result['MSG']}, status=400)

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
        if not recipeList:
            return JsonResponse({'message': 'NO_MATCHING_SEQ'}, status=400)
        return JsonResponse({'메뉴명': name, '영양성분': nutritionList, '레시피': recipeList}, status=200)
    else:
        return JsonResponse({'message': 'INVALID_HTTP_METHOD'}, status=400)
