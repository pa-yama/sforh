from django.shortcuts import render, redirect
from ..models import Post, Reaction, Comment, History
import time
from django.db.models import Count
from ..forms import commentForm

#初期表示
def detailFunc(request, post_id):
    
    template_name = 'SforH/detail.html'
    
    now = time.localtime()#現在時刻の取得
    registTime = time.strftime('%Y/%m/%d %H:%M:%S', now)#時刻のフォーマット処理
    
    #データを取得。
    postObj = Post.objects.get(post_id=post_id)#投稿idから投稿オブジェクトを取得
    
    #TODOユーザIDを取得する。
    userId = request.user.id
    
    #閲覧履歴テーブルにデータを挿入。
    historyObj = History.objects.create(
        user_id = userId,
        post_id = post_id,
        insert_timestamp = registTime,
    )
    historyObj.save()
    
    isActiveEdit = False
    #ログインユーザのIDと投稿ユーザのIDを比較。
    if userId == postObj.user.id:
        isActiveEdit = True
    
    
    #コメント内容を取得して表示させる。
    commentListObj = Comment.objects.filter(post_id=post_id)#投稿idから投稿オブジェクトを取得
    
    #各コメントのいいね数を取得する。
    goodCountForEachComment = Comment.objects.filter(post_id=post_id).values('comment_id').annotate(count=Count('reaction'))
    
    isAlreadyGoodCommentList = []
    
    #コメントごとのリアクションをリスト化する。
    for cmobj in commentListObj:
        if Reaction.objects.filter(comment_id=cmobj.comment_id).count() != 0:#コメントにリアクションが1件以上あるか
            #リアクションされているコメントを取得
            reactionObj = Reaction.objects.filter(comment_id=cmobj.comment_id)
            for obj in reactionObj:#リアクションオブジェクトをループさせる。
                if obj.user_id == userId:#対象コメントに閲覧ユーザがリアクションしているかどうか
                    isAlreadyGoodComment = {'comment_id': cmobj.comment_id, 'reaction_id' : obj.reaction_id, 'isAlreadyGood':True}
                    isAlreadyGoodCommentList.append(isAlreadyGoodComment)          
        else:
            isAlreadyGoodComment = {'comment_id': cmobj.comment_id, 'reaction_id' : 'None', 'isAlreadyGood':False}
            isAlreadyGoodCommentList.append(isAlreadyGoodComment)
    
    
    commentListObj2 = list(zip(commentListObj, goodCountForEachComment, isAlreadyGoodCommentList))#検索結果の合体
    
    isAlreadyGood = False
    reaction_id = None
    
    #この投稿のいいねリストを取得
    reactionObjs = Reaction.objects.filter(post_id=post_id, user_id=userId, reaction_target='post')
    
    #閲覧ユーザが投稿に既にリアクションしているか確認する。
    for obj in reactionObjs:
        if obj.user_id == userId:
            isAlreadyGood = True
            reaction_id = obj.reaction_id
    
    ctx = {
        'post_id': postObj.post_id,
        'title': postObj.title,
        'tag': postObj.tag,
        'text_probrem': postObj.text_probrem,
        'text_solution': postObj.text_solution,
        'reference_url': postObj.reference_url,
        "name" : postObj.user.username,
        "isActiveEdit" : isActiveEdit,
        "commentListObj" : commentListObj,
        "commentCount" : commentListObj.count(),
        "isAlreadyGood" : isAlreadyGood,
        "reaction_id" : reaction_id,
        "reactionCount" : reactionObjs.count(),
        "commentListObj2" : commentListObj2,
    }
    
    return render(request, template_name, ctx)
    



#コメントするときの処理(POSTしか無い想定)
def detailCommentFunc(request, post_id):
    
    now = time.localtime()#現在時刻の取得
    registTime = time.strftime('%Y/%m/%d %H:%M:%S', now)#時刻のフォーマット処理
    post_id = request.POST.get('post_id', None)
    
    #formにデータをセット。
    form = commentForm.CommentForm(request.POST)
    
    #バリデーション処理
    form.is_valid()
    
    #最後のコメント
    comment_nb_last = request.POST.get('comment_nb', None)
    
    #最後のコメント+1をコメント番号として追加。
    comment_nb = int(comment_nb_last) + 1
    #コメントIDの作成。(投稿ID_コメント番号の形式で作成)
    comment_id = post_id + "_" + str(comment_nb)
    
    
    #コメントテーブルにデータを挿入。
    object = Comment.objects.create(
        comment_id = comment_id,
        user_id = request.user.id,
        post_id = post_id,
        text_comment = form.cleaned_data['text_comment'],
        insert_timestamp = registTime,
        update_timestamp = registTime,
    )
    object.save()
    
    
    return redirect('detail', post_id=post_id)
    
    






#投稿にいいねするときの処理(POSTしか無い想定)
def detailGoodPostFunc(request, post_id):
    
    now = time.localtime()#現在時刻の取得
    registTime = time.strftime('%Y/%m/%d %H:%M:%S', now)#時刻のフォーマット処理
    
    post_id = request.POST.get('post_id', None)
    
    #リアクション対象が投稿の場合
        
    #リアクションテーブルにデータを挿入。(投稿にいいね)
    object = Reaction.objects.create(
        user_id = request.user.id,
        post_id = post_id,
        comment_id = None,#投稿にいいねしてる場合はいらないはず？
        good = "1",
        reaction_target = request.POST['reaction_target'],
        insert_timestamp = registTime,
        update_timestamp = registTime,
    )
    object.save()
    
    return redirect('detail', post_id=post_id)
    
    
#投稿にいいね解除するときの処理(POSTしか無い想定)
def detailUnlikePostFunc(request, post_id):
    
    reaction_id = request.POST.get('reaction_id', None)
    
    #リアクションテーブルからデータを取得。(投稿にいいね)
    Reaction.objects.filter(reaction_id=reaction_id).delete()

    return redirect('detail', post_id=post_id)
    


#コメントにいいねするときの処理(POSTしか無い想定)
def detailGoodCommentFunc(request, post_id):
    
    now = time.localtime()#現在時刻の取得
    registTime = time.strftime('%Y/%m/%d %H:%M:%S', now)#時刻のフォーマット処理
    
    post_id = request.POST.get('post_id', None)
    
        
    #リアクションテーブルにデータを挿入。(コメントにいいね)
    object = Reaction.objects.create(
        user_id = request.POST['user_id'],#TODOユーザーIDはログイン中のユーザーから取得できるようにする。
        post_id = post_id,
        comment_id = request.POST['comment_id'],#コメントidの取得。
        good = "1",
        reaction_target = request.POST['reaction_target'],
        insert_timestamp = registTime,
        update_timestamp = registTime,
    )
    object.save()
    
    return redirect('detail', post_id=post_id)
    
    
#コメントにいいね解除するときの処理(POSTしか無い想定)
def detailUnlikeCommentFunc(request, post_id):
    
    reaction_id = request.POST.get('reaction_id', None)
    
    #リアクションテーブルからデータを取得。(コメントにいいね解除)
    Reaction.objects.filter(reaction_id=reaction_id).delete()

    return redirect('detail', post_id=post_id)
    

