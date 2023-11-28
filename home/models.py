from django.db import models

# Create your models here.
import pymysql
from dotenv import load_dotenv
import os
import tensorflow as tf
from tensorflow.keras.models import load_model

load_dotenv()

# Create your models here.


def load_keras_model():
    model_path = 'C:/dishcovery/dishcovery/Dishcovery_MobileNet5532.h5'
    model = load_model(model_path)
    return model


def food_search(category, keyword):
    conn = pymysql.connect(host=os.getenv('DB_HOST'), user=os.getenv(
        'DB_USER'), password=os.getenv('DB_PASSWORD'), db=os.getenv('DB_NAME'), charset='utf8')
    cur = conn.cursor()
    sql = "SELECT `F_Name`, `F_Method`, `F_type` from food where "
    re = None
    if category == "name":
        cur.execute(sql+"F_Name = '"+keyword+"'")
    elif category == "method":
        cur.execute(sql+"F_Method = '"+keyword+"'")
    elif category == "type":
        cur.execute(sql+"F_type = '"+keyword+"'")
    else:
        cur.execute(sql+"F_Name = '"+keyword+"'")
        re = cur.fetchall()
        if not re:
            cur.execute(sql+"F_Method = '"+keyword+"'")
            re = cur.fetchall()
            if not re:
                cur.execute(sql+"F_type = '"+keyword+"'")

    res = cur.fetchall()
    if not res and re:
        res = re
    conn.commit()
    conn.close()
    return res

"""
def find_user_by_kakao(kakao_id):
    conn = pymysql.connect(host=os.getenv('DB_HOST'), user=os.getenv(
        'DB_USER'), password=os.getenv('DB_PASSWORD'), db=os.getenv('DB_NAME'), charset='utf8')
    cur = conn.cursor()
    sql = "select * from user where kakaoId = '"+str(kakao_id)+"'"
    cur.execute(sql)
    res = cur.fetchall()
    return res


def save_user_info(kakao_id, kakao_nickname):
    kakaoid = kakao_id
    kakaonickname = kakao_nickname
    user = find_user_by_kakao(kakaoid)
    # 존재하는 회원인 경우 추가로 저장 안함
    if not user:
        conn = pymysql.connect(host=os.getenv('DB_HOST'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'),
                               db=os.getenv('DB_NAME'), charset='utf8')
        cur = conn.cursor()
        sql = "INSERT INTO User (kakaoId, nickName) VALUES (" + \
            str(kakaoid)+", '"+kakaonickname+"');"
        cur.execute(sql)
        conn.commit()
        conn.close()
        
"""