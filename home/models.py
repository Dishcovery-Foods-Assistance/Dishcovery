# from django.db import models
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

# Create your models here.


def food_name():
    conn = pymysql.connect(host=os.getenv('DB_HOST'), user=os.getenv(
        'DB_USER'), password=os.getenv('DB_PASSWORD'), db=os.getenv('DB_NAME'), charset='utf8')
    cur = conn.cursor()
    sql = "SELECT * from food where F_Name"
    cur.execute(sql)
    res = cur.fetchall()
    conn.commit()
    conn.close()
    return res
