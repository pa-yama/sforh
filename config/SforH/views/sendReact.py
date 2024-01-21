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
from django.http import HttpResponseRedirect


#reactのホームに遷移する用の関数。
def sendReact(request):
    print("react画面に遷移")
    
    return HttpResponseRedirect("http://localhost:3000/")
