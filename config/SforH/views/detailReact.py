from django.shortcuts import render, redirect
from ..models import Post, Reaction, Comment, History
import time
from django.db.models import Count
from ..forms import commentForm
from django.http import JsonResponse
from ..serializers import DetailPySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer

#初期表示
@api_view(['GET'])
@renderer_classes([JSONRenderer])  # JSONレンダラーを指定
def detailFunc(request, post_id):
    
    #print("reactからの動作確認")
    #template_name = 'SforH/detail.html'
    
    now = time.localtime()#現在時刻の取得
    registTime = time.strftime('%Y/%m/%d %H:%M:%S', now)#時刻のフォーマット処理
    
    #データを取得。
    postObj = Post.objects.get(post_id=post_id)#投稿idから投稿オブジェクトを取得
    
    #TODOユーザIDを取得する。
    #userId = request.user.id#ビルド時はこっちにすればいいはず。
    userId = '1'
    
    
    #print(request.user)
    
    
    
    
    #閲覧履歴テーブルにデータを挿入。
    historyObj = History.objects.create(
        user_id = userId,
        post_id = post_id,
        insert_timestamp = registTime,
    )
    historyObj.save()
    
    #print('userId')
    #print(userId)
    
    #print('postObj.user.id')
    #print(postObj.user.id)
    
    isActiveEdit = False
    #ログインユーザのIDと投稿ユーザのIDを比較。
    if int(userId) == postObj.user.id:
        #print('比較の確認1')
        isActiveEdit = True
    
    #print('isActiveEdit')
    #print(isActiveEdit)
    
    #コメント内容を取得して表示させる。
    commentListObj = Comment.objects.filter(post_id=post_id).order_by('comment_id')#投稿idから投稿オブジェクトを取得
    

    
    #各コメントのいいね数を取得する。
    goodCountForEachComment = Comment.objects.filter(post_id=str(post_id)).values('comment_id').annotate(count=Count('reaction'))
    
    
    #print("★★★★★★★★★★")
    #print(Comment.objects.filter(post_id=str(post_id)).values('comment_id').annotate(count=Count('reaction')).query)
    #print("★★★★★★★★★★")
    
    isAlreadyGoodCommentList = []
    
    #コメントごとのリアクションをリスト化する。
    for cmobj in commentListObj:
        
        #print('返信コメントではありません')
        #print("cmobjが存在する。")
        if Reaction.objects.filter(comment_id=str(cmobj.comment_id)).count() != 0:#コメントにリアクションが1件以上あるか
            #リアクションされているコメントを取得
            #print("リアクションされているコメントが存在する。")
            reactionObj = Reaction.objects.filter(comment_id=str(cmobj.comment_id))
            
            for obj in reactionObj:#リアクションオブジェクトをループさせる。
                if obj.user_id == int(userId):#対象コメントに閲覧ユーザがリアクションしているかどうか
                    isAlreadyGoodComment = {'comment_id': cmobj.comment_id, 'reaction_id' : obj.reaction_id, 'isAlreadyGood':True}
                    isAlreadyGoodCommentList.append(isAlreadyGoodComment)
                else:
                    isAlreadyGoodComment = {'comment_id': cmobj.comment_id, 'reaction_id' : 'None', 'isAlreadyGood':False}
                    isAlreadyGoodCommentList.append(isAlreadyGoodComment)         
        else:
            #print("リアクションされているコメントが存在しない。")
            isAlreadyGoodComment = {'comment_id': cmobj.comment_id, 'reaction_id' : 'None', 'isAlreadyGood':False}
            isAlreadyGoodCommentList.append(isAlreadyGoodComment)
        
            
            
            
            
        
        
    
    #print("post_id")
    #print(post_id)
    
    #print("commentListObjの確認")
    #print(commentListObj)
    
    #print("goodCountForEachCommentの確認")
    #print(goodCountForEachComment)
    
    #print("isAlreadyGoodCommentList")
    #print(isAlreadyGoodCommentList)
    
    #commentListObj2 = list(zip(commentListObj, goodCountForEachComment, isAlreadyGoodCommentList))#検索結果の合体
    
    #print("コメントリスト2の情報を確認する。")
    #print(commentListObj2)
    
    #print("コメントリストを辞書型に変換する。")
    lastComment_id = ""
    
    commentListdictionaries = []
    
    for obj in commentListObj:
        
        comment_id_split = obj.comment_id.split('_')
        #print('comment_id : ' + obj.comment_id)
        
        #返信コメントの処理
        if len(comment_id_split) == 2:
            #print('返信コメントではありません')
        
            commentListdictionary = {}
            #print("1")
            commentListdictionary["comment_id"] = obj.comment_id
            #print("2")
            commentListdictionary["post_id"] = obj.post.post_id
            #print("3")
            commentListdictionary["user_id"] = obj.user_id
            #print("4")
            commentListdictionary["text_comment"] = obj.text_comment
            #print("5")
            commentListdictionary["insert_timestamp"] = obj.insert_timestamp
            #print("6")
            commentListdictionary["update_timestamp"] = obj.update_timestamp
            #print("7")
            
            for goodCount in goodCountForEachComment:
                if goodCount['comment_id'] == obj.comment_id:
                    commentListdictionary["count"] = goodCount['count']
            
            for isAlreadyGoodComment in isAlreadyGoodCommentList:
                if isAlreadyGoodComment['comment_id'] == obj.comment_id:
                    commentListdictionary["reaction_id"] = isAlreadyGoodComment['reaction_id']
                    commentListdictionary["isAlreadyGood"] = str(isAlreadyGoodComment['isAlreadyGood'])
            
            commentListdictionary["haveReply"] = 'False'#返信の有無
            commentListdictionary["commentReplyListdictionaries"] = []#返信リスト
            #print("10")
            lastComment_id = obj.comment_id
            
            commentListdictionaries.append(commentListdictionary)      
        
        
        
        elif len(comment_id_split) == 3:
            #print('返信コメントです')
            commentReplyListdictionary = {}
            #print("1")
            commentReplyListdictionary["comment_id"] = obj.comment_id
            #print("2")
            commentReplyListdictionary["post_id"] = obj.post.post_id
            #print("3")
            commentReplyListdictionary["user_id"] = obj.user_id
            #print("4")
            commentReplyListdictionary["text_comment"] = obj.text_comment
            #print("5")
            commentReplyListdictionary["insert_timestamp"] = obj.insert_timestamp
            #print("6")
            commentReplyListdictionary["update_timestamp"] = obj.update_timestamp
            for goodCount in goodCountForEachComment:
                if goodCount['comment_id'] == obj.comment_id:
                    commentReplyListdictionary["count"] = goodCount['count']
            
            for isAlreadyGoodComment in isAlreadyGoodCommentList:
                if isAlreadyGoodComment['comment_id'] == obj.comment_id:
                    commentReplyListdictionary["reaction_id"] = isAlreadyGoodComment['reaction_id']
                    commentReplyListdictionary["isAlreadyGood"] = str(isAlreadyGoodComment['isAlreadyGood'])
            
            #返信コメントは既存のcommentListdictionariesの中に入れ込む。
            #既存のcommentListdictionariesを回す。(このやり方だと、データがの順番とかでエラー出そうやな)
            for commentListdictionary in commentListdictionaries:
                
                comment_id_split = obj.comment_id.split('_')
                replyComment_id = comment_id_split[0] + '_' + comment_id_split[1]
                
                if commentListdictionary['comment_id'] == replyComment_id:
                
                    #print('commentListdictionary')
                    #print(commentListdictionary)
                    
                    commentListdictionary["haveReply"] = 'True'
                    
                    commentListdictionary["commentReplyListdictionaries"].append(commentReplyListdictionary)
                    commentListdictionary["lastReplyComment_id"] = obj.comment_id
                    
            
            
        

    
    #print("コメントリストを辞書型に変換終了。")
    
    #print("commentListdictionaryの確認")
    #print(commentListdictionary)
    
    #print("commentListdictionariesの確認")
    #print(commentListdictionaries)
    
    
    isAlreadyGood = False
    reaction_id = None
    
    #この投稿のいいねリストを取得
    reactionObjs = Reaction.objects.filter(post_id=post_id, user_id=userId, reaction_target='post')
    
    #print("reactionObjsの確認")
    #print(reactionObjs)
    
    
    #print("既にいいねしてるか確認する。")
    #print("閲覧ユーザIDの確認")
    #print(userId)
    
    #閲覧ユーザが投稿に既にリアクションしているか確認する。
    for obj in reactionObjs:
        #print('objのユーザIDを確認する。')
        #print(obj.user_id)
        if obj.user_id == int(userId):#数値型にキャストしないとTrueにならない。
            #print('2')
            isAlreadyGood = True
            reaction_id = obj.reaction_id
    
    #print("既にいいねしてるか確認終了。")
    
    
    return JsonResponse(
                            {
                                'message': 'Success',
                                'post_id': str(postObj.post_id),
                                'title': str(postObj.title),
                                'tag': str(postObj.tag),
                                'text_probrem': str(postObj.text_probrem),
                                'text_solution': str(postObj.text_solution),
                                'reference_url': str(postObj.reference_url),
                                "name" : str(postObj.user.username),
                                "isActiveEdit" : str(isActiveEdit),
                                "commentListObj" : str(commentListObj),
                                "commentCount" : str(commentListObj.count()),
                                
                                "lastComment_id" : str(lastComment_id),
                                
                                "isAlreadyGood" : str(isAlreadyGood),
                                "reaction_id" : str(reaction_id),
                                "reactionCount" : str(reactionObjs.count()),
                                "commentListdictionaries" : commentListdictionaries,
                            }
                        )




#コメントするときの処理(POSTしか無い想定)
@api_view(['POST'])
@renderer_classes([JSONRenderer])  # JSONレンダラーを指定
def detailCommentFunc(request, post_id):
    
    now = time.localtime()#現在時刻の取得
    registTime = time.strftime('%Y/%m/%d %H:%M:%S', now)#時刻のフォーマット処理
    #post_id = request.POST.get('post_id', None)
    
    userId = '1'#TODOユーザーIDをrequestから取得。
    
    text_comment = request.data.get('text_comment')
    
    #formにデータをセット。
    #form = commentForm.CommentForm(request.POST)
    
    #バリデーション処理
    #form.is_valid()
    
    #最後のコメント
    #comment_nb_last = request.POST.get('comment_nb', None)
    lastComment_id = request.data.get('lastComment_id')
    
    lastComment_id_split = lastComment_id.split("_")
    
    #最後のコメント+1をコメント番号として追加。
    comment_nb = int(lastComment_id_split[1]) + 1
    #コメントIDの作成。(投稿ID_コメント番号の形式で作成)
    comment_id = post_id + "_" + str(comment_nb)
    
    
    #コメントテーブルにデータを挿入。
    object = Comment.objects.create(
        comment_id = comment_id,
        #user_id = request.user.id,
        user_id = userId,
        post_id = post_id,
        #text_comment = form.cleaned_data['text_comment'],
        text_comment = text_comment,
        insert_timestamp = registTime,
        update_timestamp = registTime,
    )
    object.save()
    
    
    return redirect('detail', post_id=post_id)
    







#投稿にいいねするときの処理(POSTしか無い想定)
@api_view(['POST'])
@renderer_classes([JSONRenderer])  # JSONレンダラーを指定
def detailGoodPostFunc(request, post_id):
    
    print('確認1')
    
    now = time.localtime()#現在時刻の取得
    registTime = time.strftime('%Y/%m/%d %H:%M:%S', now)#時刻のフォーマット処理
    
    userId = '1'#TODOユーザーIDをrequestから取得。
    
    print('データ挿入内容の確認')
    
    print(userId)
    print(post_id)
    print(None)
    print("1")
    print('post')
    print(registTime)
    print(registTime)
    
    print('データ挿入内容の確認終了')
    
    #リアクション対象が投稿の場合
        
    #リアクションテーブルにデータを挿入。(投稿にいいね)
    object = Reaction.objects.create(
        user_id = userId,
        post_id = post_id,
        comment_id = None,#投稿にいいねしてる場合はいらないはず？
        good = "1",
        #reaction_target = request.POST['reaction_target'],
        reaction_target = 'post',
        insert_timestamp = registTime,
        update_timestamp = registTime,
    )
    object.save()
    
    return redirect('detail', post_id=post_id)
    #return JsonResponse({'message': 'Success'})
    
    
    
#投稿にいいね解除するときの処理(POSTしか無い想定)
@api_view(['POST'])
@renderer_classes([JSONRenderer])  # JSONレンダラーを指定
def detailUnlikePostFunc(request, post_id):
    
    print("いいね解除確認1")
    print(request.data)
    reaction_id = request.data.get('reaction_id')
    
    print("reaction_idの確認")
    print(reaction_id)
    
    #reaction_id = request.POST.get('reaction_id', None)
    
    #リアクションテーブルからデータを取得。(投稿にいいね)
    Reaction.objects.filter(reaction_id=reaction_id).delete()

    return redirect('detail', post_id=post_id)
    


#コメントにいいねするときの処理(POSTしか無い想定)
@api_view(['POST'])
@renderer_classes([JSONRenderer])  # JSONレンダラーを指定
def detailGoodCommentFunc(request, post_id):
    
    
    print('確認1')
    
    now = time.localtime()#現在時刻の取得
    registTime = time.strftime('%Y/%m/%d %H:%M:%S', now)#時刻のフォーマット処理
    
    #post_id = request.POST.get('post_id', None)
    userId = '1'
    comment_id = request.data.get('comment_id')
    
    print('Reactからおくられた内容の確認')
    print('comment_id : ' + comment_id)
    print('post_id : ' + post_id)
    
        
    #リアクションテーブルにデータを挿入。(コメントにいいね)
    object = Reaction.objects.create(
        user_id = userId,#TODOユーザーIDはログイン中のユーザーから取得できるようにする。
        post_id = post_id,
        #comment_id = request.POST['comment_id'],#コメントidの取得。
        comment_id = comment_id,
        good = "1",
        reaction_target = 'comment',
        insert_timestamp = registTime,
        update_timestamp = registTime,
    )
    object.save()
    
    print('確認2')
    
    return redirect('detail', post_id=post_id)
    '''
    return JsonResponse(
                            {
                                'message': 'Success',
                                'post_id': str(post_id),
                            }
                        )
    '''
    
    
#コメントにいいね解除するときの処理(POSTしか無い想定)
@api_view(['POST'])
@renderer_classes([JSONRenderer])  # JSONレンダラーを指定
def detailUnlikeCommentFunc(request, post_id):
    
    reaction_id = request.data.get('comment_id')
    
    #リアクションテーブルからデータを取得。(コメントにいいね解除)
    Reaction.objects.filter(reaction_id=reaction_id).delete()

    return redirect('detail', post_id=post_id)
    




#コメントするときの処理(POSTしか無い想定)
@api_view(['POST'])
@renderer_classes([JSONRenderer])  # JSONレンダラーを指定
def detailReplyFunc(request, post_id):
    
    now = time.localtime()#現在時刻の取得
    registTime = time.strftime('%Y/%m/%d %H:%M:%S', now)#時刻のフォーマット処理
    #post_id = request.POST.get('post_id', None)
    
    userId = '1'#TODOユーザーIDをrequestから取得。
    
    text_comment = request.data.get('text_comment')
    
    #formにデータをセット。
    #form = commentForm.CommentForm(request.POST)
    
    #バリデーション処理
    #form.is_valid()
    
    #最後のコメント
    #comment_nb_last = request.POST.get('comment_nb', None)
    #comment_nb_last = request.data.get('comment_nb')
    
    #返信するコメントのID
    replyComment_id = request.data.get('comment_id')
    
    
    #「4_1」なら「4_1_1」
    #「4_1_1」なら「4_1_2」
    
    #最後のコメント+1をコメント番号として追加。
    comment_nb = 1
    
    comment_id = ''
    
    splitReplyComment_id = replyComment_id.split('_')
    
    print(splitReplyComment_id)
    print(len(splitReplyComment_id))
    
    
    
    if len(splitReplyComment_id)  == 2:
        #返信の一件も無い場合の処理
        print('返信無し')
        #コメントIDの作成。(投稿ID_コメント番号_返信番号の形式で作成)
        comment_id = replyComment_id + "_" + str(comment_nb)
    
    elif len(splitReplyComment_id) == 3:
        #返信が一件以上存在する場合の処理
        print('返信有り')
        print(splitReplyComment_id[2])
        comment_nb = int(splitReplyComment_id[2]) + 1
        comment_id = splitReplyComment_id[0] + '_' + splitReplyComment_id[1] + '_' + str(comment_nb)
        
        
    
    
    
    
    
    
    
    
    print('登録するreaction_id : ' + comment_id)
    
    
    
    #コメントテーブルにデータを挿入。
    object = Comment.objects.create(
        comment_id = comment_id,
        #user_id = request.user.id,
        user_id = userId,
        post_id = post_id,
        #text_comment = form.cleaned_data['text_comment'],
        text_comment = text_comment,
        insert_timestamp = registTime,
        update_timestamp = registTime,
    )
    object.save()
    
    
    return redirect('detail', post_id=post_id)
    






#返信コメントに返信するときの処理(POSTしか無い想定)
@api_view(['POST'])
@renderer_classes([JSONRenderer])  # JSONレンダラーを指定
def detailReplyToReplyFunc(request, post_id):
    
    now = time.localtime()#現在時刻の取得
    registTime = time.strftime('%Y/%m/%d %H:%M:%S', now)#時刻のフォーマット処理
    #post_id = request.POST.get('post_id', None)
    
    userId = '1'#TODOユーザーIDをrequestから取得。
    
    text_comment = request.data.get('text_comment')
    
    #formにデータをセット。
    #form = commentForm.CommentForm(request.POST)
    
    #バリデーション処理
    #form.is_valid()
    
    #最後のコメント
    #comment_nb_last = request.POST.get('comment_nb', None)
    #comment_nb_last = request.data.get('comment_nb')
    
    #返信するコメントのID
    replyComment_id = request.data.get('comment_id')
    
    
    #「4_1」なら「4_1_1」
    #「4_1_1」なら「4_1_2」
    
    #最後のコメント+1をコメント番号として追加。
    comment_nb = 1
    
    comment_id = ''
    
    splitReplyComment_id = replyComment_id.split('_')
    
    print(splitReplyComment_id)
    print(len(splitReplyComment_id))
    
    
    '''
    if len(splitReplyComment_id)  == 2:
        #返信の一件も無い場合の処理
        print('返信無し')
        #コメントIDの作成。(投稿ID_コメント番号_返信番号の形式で作成)
        comment_id = replyComment_id + "_" + str(comment_nb)
    
    elif len(splitReplyComment_id) == 3:
        #返信が一件以上存在する場合の処理
        print('返信有り')
        print(splitReplyComment_id[2])
        comment_nb = int(splitReplyComment_id[2]) + 1
        comment_id = splitReplyComment_id[0] + '_' + splitReplyComment_id[1] + '_' + str(comment_nb)
    '''
        
    print(splitReplyComment_id[2])
    comment_nb = int(splitReplyComment_id[2]) + 1
    comment_id = splitReplyComment_id[0] + '_' + splitReplyComment_id[1] + '_' + str(comment_nb)
    
    
    
    
    
    
    
    print('登録するreaction_id : ' + comment_id)
    
    
    
    #コメントテーブルにデータを挿入。
    object = Comment.objects.create(
        comment_id = comment_id,
        #user_id = request.user.id,
        user_id = userId,
        post_id = post_id,
        #text_comment = form.cleaned_data['text_comment'],
        text_comment = text_comment,
        insert_timestamp = registTime,
        update_timestamp = registTime,
    )
    object.save()
    
    
    return redirect('detail', post_id=post_id)



