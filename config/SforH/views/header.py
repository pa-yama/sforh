from django.shortcuts import render
from ..models import Post
from ..models import History
from django.db.models import Count
from django.db.models import Q
import re
from ..serializers import PostSerializer
from ..serializers import DetailSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer


# request.user.is_authenticated　これでセッションとれるかも

@renderer_classes([JSONRenderer])  # JSONレンダラーを指定
def getSession(request): 
    #ユーザーのログイン状態を取得
    userSession = request.user.is_authenticated
    return JsonResponse({'message': 'Success', 'is_authenticated': userSession,})