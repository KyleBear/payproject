from django.shortcuts import render
import pdb
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Owner, Product
from .serializers import OwnerSerializer, ProductSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password,make_password
# from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from django.core.cache import cache
import pytz
from datetime import datetime, timedelta
# 토큰 함수
import jwt
from functools import wraps
from rest_framework.pagination import CursorPagination
from django.http import JsonResponse
from django.db.models import Q


def cur_time_asia():
    asia_seoul = pytz.timezone('Asia/Seoul')
    now_asia_seoul = datetime.now(asia_seoul)
    return now_asia_seoul

def generate_token(phone_number):
    # 토큰의 만료 시간 설정
    now_asia_seoul = cur_time_asia()
    # expiration_time = now_asia_seoul + timedelta(hours=12)
    expiration_time = now_asia_seoul + timedelta(hours=24)
    payload = {
        'phone_number': phone_number,
        'exp': expiration_time
    }
    # 시크릿 키 설정
    secret_key = 'payhere_secret_key'
    # 토큰 생성
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    #request.session['token'] = token
    return token

#토큰을 변수로 받음 - 해당 토큰의 유효성만 검증 (만료시간, 토큰 key 값 검증.)
def verify_token(token):
    secret_key = 'payhere_secret_key'
    try:
        # 토큰의 유효성 검증 - 해당 키로 파싱되는지.
        decode_token = jwt.decode(token, secret_key, algorithms=['HS256'])
        # return decode_token
        return token
    except jwt.ExpiredSignatureError:
        return 'token expired'
    except jwt.InvalidTokenError:
        return False


def token_required(f):
    @wraps(f)
    # def decorator(request, *args, **kwargs):
    def decorator(self, request, *args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            # 헤더에서 "Bearer <token>" 형식의 값을 가져옵니다.
            auth_header = request.headers['Authorization']
            # 값을 공백으로 분리합니다.
            auth_parts = auth_header.split()
            
            # 첫 번째 부분이 "Bearer"이고, 두 번째 부분(실제 토큰 값)이 있는지 확인합니다.
            if len(auth_parts) == 2 and auth_parts[0].lower() == "bearer":
                token = auth_parts[1]
            else:
                json_response = default_result( 401,False, 'Invalid token')
                return JsonResponse(json_response, status=401)        
        if not token:
            json_response = default_result( 401,False, 'Token is missing')
            return JsonResponse(json_response, status=401)
        
        try:
            # verify_token 함수를 호출하되, 토큰 값 부분만 넘겨줍니다.
            data = verify_token(token)
            if data == 'token expired':
                json_response = default_result( 401,False, 'Token is expired')
                return JsonResponse(json_response, status=401)
            elif data == False:
                json_response = default_result( 401,False, 'Token is invalid')
                return JsonResponse(json_response, status=401)                
        except:
            json_response = default_result( 401,False, 'Token is invalid')
            return JsonResponse(json_response, status=401)
            
        # return f(request, *args, **kwargs)
        return f(self, request, *args, **kwargs)
# 토큰

class LogoutView(APIView):
    def post(self, request):
        token_key = request.data.get('token')
        if token_key:
            try:
                token = Token.objects.get(key=token_key)
                # 해당 토큰을 삭제하여 로그아웃 처리
                token.delete()
                return Response({"detail": "로그아웃이 성공적으로 처리되었습니다."}, status=status.HTTP_200_OK)
            except Token.DoesNotExist:
                return Response({"detail": "유효하지 않은 토큰입니다."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "토큰을 제공해야 합니다."}, status=status.HTTP_400_BAD_REQUEST)



class CustomCursorPagination(CursorPagination):
    page_size = 10
    ordering = 'id'  # 기본적으로 id를 기준으로 페이지네이션

class OwnerSignupView(APIView):
    def post(self, request):
        serializer = OwnerSerializer(data=request.data)
        if serializer.is_valid():
            password = make_password(serializer.validated_data['password'])
            serializer.validated_data['password'] = password
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "meta": {"code": 400, "message": "잘못된 요청입니다."},
                "data": {}
            }, status=status.HTTP_400_BAD_REQUEST)

class OwnerLoginView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        owner = Owner.objects.filter(phone_number=phone_number).first()
        if owner:
            if owner.check_password(password):
                SECRET_KEY = 'payhere_secret_key'
                token = generate_token(phone_number)
                token = verify_token(token)

                return Response({
                    "meta": {"code": 200, "message": "ok"},
                    "data": {"owner_id": owner.id,
                    'user_token': token}
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "meta": {"code": 400, "message": "잘못된 요청입니다"},
                    "data": {}
                }, status=status.HTTP_400_BAD_REQUEST)


class ProductListView(APIView):
    def get(self, request):
        try:
            paginator = CustomCursorPagination()
            products = Product.objects.all()
            result_page = paginator.paginate_queryset(products, request)
            serializer = ProductSerializer(result_page, many=True)        
            return Response({
                    "meta": {"code": 200, "message": "ok"},
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
        except:
            return Response({
                    "meta": {"code": 400, "message": "잘못된 요청입니다."},
                    "data": {}
                }, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request):
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "meta": {"code": 200, "message": "ok"},
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else: 
            errors = serializer.errors
            return Response({
                "meta": {"code": 400, "message": "잘못된 요청입니다."},
                "data": {}
            }, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk) #model 에서 product 확인.
        serializer = ProductSerializer(product)
        return Response({
            "meta": {"code": 200, "message": "ok"},
            "data": {"product": serializer.data}
        })

    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            # pdb.set_trace()
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "meta": {"code": 200, "message": "상세 정보가 성공적으로 업데이트되었습니다."},
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({"meta": {"code": 404, "message": "해당 제품을 찾을 수 없습니다."}}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request,pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def convert_to_initial(c):
    """주어진 한글 문자 c를 초성으로 변환하는 함수"""
    CHOSUNG_START = 44032
    CHOSUNG_BASE = 588
    CHOSUNG_LIST = [
        'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ',
        'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
    ]
    
    if not '가' <= c <= '힣':
        return c
    
    return CHOSUNG_LIST[(ord(c) - CHOSUNG_START) // CHOSUNG_BASE]

def search_product(request,keyword):
    # keyword = request.GET.get('keyword', '')
    # keyword = keyword

    # 초성으로 검색할 키워드 생성
    chosung_keyword = ''.join(convert_to_initial(c) for c in keyword)
    # Q 객체를 사용하여 이름에 대한 like 검색과 초성검색을 지원
    products = Product.objects.filter(
        Q(name__icontains=keyword) | 
        Q(name__icontains=chosung_keyword)
    )
    # 검색 결과를 JSON 형식으로 반환
    data = {
        'products': list(products.values())
    }
    return JsonResponse(data)
