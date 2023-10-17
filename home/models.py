from django.db import models
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

# Create your models here.


def food_search(category, keyword):
    conn = pymysql.connect(host=os.getenv('DB_HOST'), user=os.getenv(
        'DB_USER'), password=os.getenv('DB_PASSWORD'), db=os.getenv('DB_NAME'), charset='utf8')
    cur = conn.cursor()
    sql = "SELECT `F_Name`, `F_Method`, `F_type` from food where "
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
    if not res:
        res = re
    conn.commit()
    conn.close()
    return res


def saveUserInfo(kakao_id, kakao_nickname):
    kakaoid = kakao_id
    kakaonickname= kakao_nickname
    conn = pymysql.connect(host=os.getenv('DB_HOST'), user=os.getenv(
        'DB_USER'), password=os.getenv('DB_PASSWORD'), db=os.getenv('DB_NAME'), charset='utf8')
    cur = conn.cursor()
    sql = "INSERT INTO User (kakaoId, nickName) VALUES ("+str(kakaoid)+", '"+kakaonickname+"');"
    cur.execute(sql)
    conn.commit()
    conn.close()


