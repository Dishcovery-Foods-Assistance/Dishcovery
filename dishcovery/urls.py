# from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from foods.views import classify_image

from foods import views

app_name = 'foods'

urlpatterns = [
    path('', views.main_home, name='main_home'),
    path('dbSearch/', views.dbSearch, name='dbSearch'),
    path('Search/', views.apiSearch, name='Search'),
    path('Search/detail/', views.foodDetail, name='foodDetail'),
    path('chatbot/', views.food_recommendation, name='chatbot'),
    path('chatbot/assistance/', views.food_assistance, name='assistance'),
    path('classify_image/', views.classify_image, name='classify_image'),
    path('food_search/', views.Search_food, name='food_search'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)