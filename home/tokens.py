import os
import datetime
import jwt
from home import models


def generate_token(payload):
    access_token_payload = {
        "id": payload,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1), #만료시간
        "iat": datetime.datetime.utcnow(), #발급시간
    }
    access_token = jwt.encode(
        access_token_payload, os.getenv("JWT_SECRET_KEY"), algorithm=os.getenv("ALGORITHM")
    )

    refresh_token_payload = {
        "id": payload,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
        "iat": datetime.datetime.utcnow(),
    }
    refresh_token = jwt.encode(
        refresh_token_payload, os.getenv("REFRESH_SECRET_KEY"), algorithm=os.getenv("ALGORITHM")
    )

    token_build = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "kakao_id": payload
    }

    return token_build


def verify_token(token):
    try:
        secret_key = os.getenv("JWT_SECRET_KEY")
        # 토큰 검증 및 디코딩
        decoded_token = jwt.decode(token, secret_key, algorithms=[os.getenv("ALGORITHM")])

        # 디코딩된 토큰에서 필요한 정보 추출
        kakao_id = decoded_token['id']

        user = models.findUserByKakao(kakao_id)
        # 유효한 토큰인 경우 사용자 정보 반환
        if user:
            return "SUCCESS"
        else:
            return "User Not Exist"
    except jwt.ExpiredSignatureError:
        # 토큰의 유효 기간이 만료된 경우
        return "Token expired"

    except jwt.InvalidTokenError:
        # 유효하지 않은 토큰인 경우
        return "Invalid token"


def refresh(r_token):
    try:
        secret_key = os.getenv("REFRESH_SECRET_KEY")
        decoded_token = jwt.decode(r_token, secret_key, algorithms=[os.getenv("ALGORITHM")])
        kakao_id = decoded_token['id']
        user = models.findUserByKakao(kakao_id)
        if user:
            refreshed = generate_token(kakao_id)
            res = ({
                'message': 'SUCCESS',
                'token': refreshed
            })
            return res
        else:
            res = ({'message': 'User Not Exist'})
            return res
    except jwt.ExpiredSignatureError:
        res = ({'message': 'Token expired'})
        return res
