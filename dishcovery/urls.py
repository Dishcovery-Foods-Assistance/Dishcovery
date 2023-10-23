"""
URL configuration for dishcovery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from home import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'home'

urlpatterns = [
    path('', views.main_home, name='main_home'),
    path('search/', views.dbSearch, name='search'),
    path('recipe/', views.apiSearch, name='recipe'),
    path('recipe/detail/', views.foodDetail, name='detail'),
    path('kakao/', views.kakaoLogin, name='login'),
    path('kakao/callback/', views.KakaoCallbackView.as_view(), name='kakao_callback'),
    path('token/verify/', views.verify_token, name='verify_token'),
    path('token/refresh/', views.token_refresh, name='token_refresh'),

    path('chatbot/', views.food_recommendation, name='token_refresh'),
    path('chatbot/assistance/', views.food_assistance, name='token_refresh')
    #    path('logIn', views.logIn),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
