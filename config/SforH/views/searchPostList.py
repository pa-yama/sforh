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

#検索一覧
def searchPostList(request):
    template_name = 'SforH/search_post.html'
    ctx = {}
    qs = Post.objects.all()

    #subquery  = History.objects.values('post').annotate(count=Count('post')).order_by('-count')

    #閲覧数が多い順にデータを表示する。
    #qs = getHistoryCount(qs)
    
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


#class test2(viewsets.ModelViewSet):
@api_view(['POST'])
@renderer_classes([JSONRenderer])  # JSONレンダラーを指定
def searchPost(request):
    data = Post.objects.all()
    #data = Post.objects.all().select_related('user')
    print('sql')
    print(data.query)


    #goodCountForEachComment = Comment.objects.filter(post_id=str(post_id)).values('comment_id').annotate(count=Count('reaction'))

    requestData = request.data.get('searchTitle')
    requestTag = request.data.get('searchTag')
    
    print('確認')
    print(requestData)
    print(requestTag)
    
    if requestData is not None or requestTag is not None:
        #スペース重複を削除/区切って配列格納
        requestData = re.escape(' '.join(requestData.split()))
        #requestTag = re.escape(' '.join(requestTag.split()))
        
        #この投稿のいいねリストを取得
        #日付とユーザー名とプロフィール画像
        #reactionObjs = Reaction.objects.filter(post_id=post_id, user_id=userId, reaction_target='post')

        titles_array = requestData.split()
        #tags_array = requestTag.split()
        print(titles_array)
        
        #検索値リプレース
        titleResult = []
        #tagResult = []
        for title in titles_array:
            title = title.replace("\\", "")
            titleResult.append(title)
            print(title)
        

        conditions = Q(*[Q(title__icontains=title) for title in titleResult]) & Q(tag__icontains = requestTag)
        data = Post.objects.filter(conditions)

    #閲覧数順に並び替え
    #data = getHistoryCount(data)
    #index = 0
    #if 0 <= index < len(data):
        #return JsonResponse({'message': 'Success',
                            #'post_id':  data[index]["post_id"],
                            #'title': data[index]["title"],
                            #'tag': data[index]["tag"], 
                            #'username': data[index]["user.username"],
                            #'insert_timestamp': data[index]["insert_timestamp"]}),
    #else:
        #return JsonResponse({"error": "Index out of range"}, status=400)


    serializer= PostSerializer(data, many=True)
    return Response(serializer.data)
    
    

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
                              'post_tag': postObj.tag, 'post_user': postObj.user.username})
        
