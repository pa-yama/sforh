from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from .models import User
from .models import Post
from .models import Post_Tmp
from .models import Comment
from .models import Reaction
from .models import History
from .models import Profile
from .forms import SearchPostForm
from django.db.models import Count
from django.db.models import Q
from django.db import models 
from django.db.models import FilteredRelation
from django.db.models import Subquery
import re
from .serializers import PostSerializer
from .serializers import DetailSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

# Create your views here.
class ListUserView(ListView):
    template_name = 'SforH/user_list.html'
    model = User

#検索一覧
def searchPostList(request):
    template_name = 'SforH/search_post.html'
    ctx = {}
    qs = Post.objects.all()

    subquery  = History.objects.values('post').annotate(count=Count('post')).order_by('-count')

    #閲覧数が多い順にデータを表示する。
    qs = getHistoryCount(qs)
    
    #タイトル,タグで検索実行
    if 'title' in request.GET or 'tag' in request.GET:
        
        #検索された値を取得
        titles = request.GET.get('title', None)      
        tags = request.GET.get('tag', None)

        #スペース重複を削除/区切って配列格納
        titles = re.escape(' '.join(titles.split()))
        tags = re.escape(' '.join(tags.split()))
        titles_array = titles.split()
        tags_array = tags.split()
        
        #検索値リプレース
        titleResult = []
        tagResult = []
        for title in titles_array:
            title = title.replace("\\", "")
            titleResult.append(title)
        for tag in tags_array:
            tag = tag.replace("\\", "")
            tagResult.append(tag)

        titleSearch = Post.objects.filter(*[Q(title__icontains=title) for title in titleResult]) 
        tagSearch = Post.objects.filter(*[Q(tag__icontains=tag) for tag in tagResult])
        
        conditions = Q(*[Q(title__icontains=title) for title in titleResult]) & Q(*[Q(tag__icontains=tag) for tag in tagResult])
        qs = Post.objects.filter(conditions)
        #qs = Post.objects.filter(tagSearch)
        print(qs.query)

        #閲覧数が多い順にデータを表示する。
        qs = getHistoryCount(qs)

    #検索が行われた場合は検索結果をqsを上書き
    ctx["object_list"] = qs

    return render(request, template_name, ctx)

#詳細画面へ遷移
def detailFunc(request):
    post_id = request.GET.get('post_id', None)
    prevScreenName = request.GET.get('prevScreenName', None)
    template_name = 'SforH/detail.html'
    ctx = {}
    return render(request, template_name, ctx)


#閲覧数順に検索結果を表示
def getHistoryCount(qs):
    historyResult = History.objects.values('post').annotate(count=Count('post')).order_by('-count')
    result_list = []
    history_empty_list = []
    for history in historyResult:
        for q in qs:
            if history['post'] == q.post_id:
                result_list.append(q.post_id)
            if not historyResult.filter(post=q.post_id).exists():
                history_empty_list.append(q.post_id)
    for history_empty in history_empty_list:
        result_list.append(history_empty)
    qs = sorted(qs, key=lambda post: result_list.index(post.post_id))
    return qs

def getSearchRequest(titles,tags):
    titles = re.escape(' '.join(titles.split()))
    titles_array = titles.split()

    print(titles_array)
    searchResult = ''
    for index, title in enumerate(titles_array):
        if index == len(titles_array) - 1:
            title = title.replace("\\", "")
            searchResult += 'title__icontains = ' + title
        else:
            title = title.replace("\\", "")
            print(title)
            searchResult += 'title__icontains = ' + title + ', '
    print('連結後' + searchResult)

    return searchResult

def my_view(request):
    return render(request, 'index.html')


class test2(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class test3(APIView):
    def post(self, request):
        #POSTリクエスト jsonデータ受け取り
        data = request.data
        post_id = data['id']
        print('レスポンスデータ確認')
        print(data)
        postObj = Post.objects.get(post_id=post_id)
        print(postObj)
        return JsonResponse({'message': 'Success', 'post_title': postObj.title,
                              'post_tag': postObj.tag, 'post_user': postObj.user.name})
        