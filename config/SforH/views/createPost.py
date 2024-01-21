from django.http import HttpResponse
from django.shortcuts import render, redirect
from ..forms.createPostTmpFrom import CreatePostTmpForm
from ..models import Post
from ..models import Post_Tmp
import time

#投稿作成・編集画面のview

#ヘッダーから遷移した時の処理
def fromHeaderFunc(request):
    
    #GETリクエストの場合
    #GETの場合START-----------------------------------------------------------
    if request.method == 'GET':
        
        template_name = 'SforH/create_post.html'#htmlファイルの名前
            
        form = CreatePostTmpForm()
        ctx = {"form": form}
        return render(request, template_name, ctx)
    #GETの場合END-----------------------------------------------------------
    
    #POSTリクエストの場合
    #POSTの場合START-----------------------------------------------------------
    elif request.method == 'POST':
        
        print("新規登録確認")
        
        template_name = 'SforH/create_post.html'
        
        now = time.localtime()#現在時刻の取得
        registTime = time.strftime('%Y/%m/%d %H:%M:%S', now)#時刻のフォーマット処理
        
        #formにデータをセット。
        form = CreatePostTmpForm(request.POST)
        
        print("テスト1")
        
        #データが不正な場合、画面に戻る。    
        if not form.is_valid():
            ctx = {"form": form}
            return render(request, template_name, ctx)
        
        print("テスト2")
        
        #一時保存ボタン押下時の処理
        if request.POST['submit'] == '一時保存':
            print("一時保存")
            #投稿一時テーブルにデータを挿入。
            object = Post_Tmp.objects.create(
                user_id = request.user.id,
                title = form.cleaned_data['title'],
                tag = form.cleaned_data['tag'],
                text_probrem = form.cleaned_data['text_probrem'],
                text_solution = form.cleaned_data['text_solution'],
                reference_url = form.cleaned_data['reference_url'],
                insert_timestamp = registTime,
                update_timestamp = registTime
            )
            object.save()

        #投稿ボタン押下時の処理
        elif request.POST['submit'] == '投稿':
            print("投稿")
            #投稿一時テーブルにデータを挿入。
            object = Post_Tmp.objects.create(
                user_id = request.user.id,
                title = form.cleaned_data['title'],
                tag = form.cleaned_data['tag'],
                text_probrem = form.cleaned_data['text_probrem'],
                text_solution = form.cleaned_data['text_solution'],
                reference_url = form.cleaned_data['reference_url'],
                insert_timestamp = registTime,
                update_timestamp = registTime,
                already_post_fg = True
            )
            object.save()
        
            #投稿一時テーブルの最新データを取得(#TODO複数ユーザーが同時に操作したら変になる可能性あるかも？)
            ptObj = Post_Tmp.objects.all().last()
            #投稿テーブルにデータを追加
            object = Post.objects.create(
                post_id = ptObj.post_id,
                user = ptObj.user,
                title = ptObj.title,
                tag = ptObj.tag,
                text_probrem = ptObj.text_probrem,
                text_solution = ptObj.text_solution,
                reference_url = ptObj.reference_url,
                insert_timestamp = ptObj.insert_timestamp,
                update_timestamp = ptObj.update_timestamp
            )
            object.save()
        
        #ctx = {"form": form}
        #return render(request, template_name, ctx)
        return redirect('search-post')
    
    
    
    #POSTの場合END-----------------------------------------------------------
    #未対応のメソッド
    else:
        return HttpResponse('不正なメソッドです', status=500)


#詳細画面から遷移した時の処理
def fromDetailFunc(request):
    
    #GETリクエストの場合
    #GETの場合START-----------------------------------------------------------
    if request.method == 'GET':
        
        template_name = 'SforH/create_post.html'#htmlファイルの名前
        
        postId = request.GET.get('post_id', None)#リクエストパラメーターから投稿idを取得
            
        print("detailから受け取った投稿ID : " + postId)
        
        #送信されたIDの投稿が存在しない場合エラー
        if not Post_Tmp.objects.filter(post_id=postId).exists:
            errorMsg = "投稿が存在しません。"
            ctx = {"errorMsg": errorMsg}
            return render(request, template_name, ctx)
        
        postObj = Post.objects.get(post_id=postId)#投稿idから投稿オブジェクトを取得
        
        #フォームの初期値に取得した投稿オブジェクトのデータをセット
        initial_values = {
                        'post_id': postObj.post_id,
                        'user': postObj.user.id,
                        'title': postObj.title,
                        'tag': postObj.tag,
                        'text_probrem': postObj.text_probrem,
                        'text_solution': postObj.text_solution,
                        'reference_url': postObj.reference_url,
                        }
        
        form = CreatePostTmpForm(initial_values)
        ctx = {"form": form, "postId": postId}
        return render(request, template_name, ctx)
    #GETの場合END-----------------------------------------------------------
        
    
    #POSTリクエストの場合
    #POSTの場合START-----------------------------------------------------------
    elif request.method == 'POST':
        
        template_name = 'SforH/create_post.html'
        
        now = time.localtime()#現在時刻の取得
        registTime = time.strftime('%Y/%m/%d %H:%M:%S', now)#時刻のフォーマット処理
        
        #formにデータをセット。
        form = CreatePostTmpForm(request.POST)

        #データが不正な場合、画面に戻る。
        if not form.is_valid():
            ctx = {"form": form}
            return render(request, template_name, ctx)
        
        #投稿IDの取得
        postId = request.POST.get("postId", None)
        
        #一時保存ボタン押下の場合
        #投稿一時保存テーブルにのみデータを挿入する。
        if request.POST['submit'] == '一時保存':
            #投稿一時テーブルにデータを挿入。
            object = Post_Tmp.objects.create(
                user_id = request.user.id,
                title = form.cleaned_data['title'],
                tag = form.cleaned_data['tag'],
                text_probrem = form.cleaned_data['text_probrem'],
                text_solution = form.cleaned_data['text_solution'],
                reference_url = form.cleaned_data['reference_url'],
                insert_timestamp = registTime,
                update_timestamp = registTime
            )
            object.save()
        
        #投稿ボタン押下の場合
        #投稿一時保存テーブルと投稿テーブルにデータを挿入する。
        elif request.POST['submit'] == '投稿':
            object = Post_Tmp.objects.create(
                user_id = request.user.id,
                title = form.cleaned_data['title'],
                tag = form.cleaned_data['tag'],
                text_probrem = form.cleaned_data['text_probrem'],
                text_solution = form.cleaned_data['text_solution'],
                reference_url = form.cleaned_data['reference_url'],
                insert_timestamp = registTime,
                update_timestamp = registTime,
                already_post_fg = True
            )
            object.save()
        
            #投稿一時テーブルの最新データを取得
            ptObj = Post_Tmp.objects.all().last()
            #投稿テーブルにデータを追加
            object = Post.objects.create(
                post_id = ptObj.post_id,
                user = ptObj.user,
                title = ptObj.title,
                tag = ptObj.tag,
                text_probrem = ptObj.text_probrem,
                text_solution = ptObj.text_solution,
                reference_url = ptObj.reference_url,
                insert_timestamp = ptObj.insert_timestamp,
                update_timestamp = ptObj.update_timestamp
            )
            object.save()
            #投稿テーブルから前の投稿を削除する。
            Post.objects.filter(post_id=postId).delete()
        
        ctx = {"form": form, "postId": postId}
        return render(request, template_name, ctx)
    
    
    #POSTの場合END-----------------------------------------------------------
    #未対応のメソッド
    else:
        return HttpResponse('不正なメソッドです', status=500)



#一時保存リストから遷移した時の処理
def fromTmpListFunc(request):
    
    template_name = 'SforH/create_post.html'#htmlファイルの名前
    
    #GETリクエストの場合
    #GETの場合START-----------------------------------------------------------
    if request.method == 'GET':
        
        postId = request.GET.get('post_id', None)#リクエストパラメーターから投稿idを取得
            
        #既投稿フラグを確認し、Trueの場合エラー
        if Post_Tmp.objects.filter(post_id=postId, already_post_fg=False).exists:
            errorMsg = "既に投稿されています。"
            ctx = {"errorMsg": errorMsg}
            return render(request, template_name, ctx)
        
        
        postObj = Post_Tmp.objects.get(post_id=postId, already_post_fg=False)#投稿idから投稿オブジェクトを取得
        
        #フォームの初期値に取得した投稿オブジェクトのデータをセット
        initial_values = {
                        'post_id': postObj.post_id,
                        'user': postObj.user.user_id,
                        'title': postObj.title,
                        'tag': postObj.tag,
                        'text_probrem': postObj.text_probrem,
                        'text_solution': postObj.text_solution,
                        'reference_url': postObj.reference_url,
                        }
    
        postObj = Post_Tmp.objects.get(post_id=postId)
        form = CreatePostTmpForm(initial_values)
        ctx = {"form": form, "postId": postId}
        return render(request, template_name, ctx)
    
    #GETの場合END-----------------------------------------------------------
        
    
    #POSTリクエストの場合
    #POSTの場合START-----------------------------------------------------------
    elif request.method == 'POST':
        template_name = 'SforH/create_post.html'
        
        now = time.localtime()#現在時刻の取得
        registTime = time.strftime('%Y/%m/%d %H:%M:%S', now)#時刻のフォーマット処理
        #formにデータをセット。
        form = CreatePostTmpForm(request.POST)
        #データが不正な場合、画面に戻る。
        if not form.is_valid():
            ctx = {"form": form}
            return render(request, template_name, ctx)
        
        #投稿IDの取得
        postId = int(request.POST.get('postId', None))
        
        #一時保存ボタン押下の場合
        #投稿一時保存テーブルのデータを更新する。
        if request.POST['submit'] == '一時保存':
            #投稿一時テーブルのデータを更新。
            object = Post_Tmp.objects.get(post_id=postId)
            object.title = form.cleaned_data['title']
            object.tag = form.cleaned_data['tag']
            object.text_probrem = form.cleaned_data['text_probrem']
            object.text_solution = form.cleaned_data['text_solution']
            object.reference_url = form.cleaned_data['reference_url']
            object.update_timestamp = registTime
            
            object.save()#更新の反映
        
        #投稿ボタン押下の場合
        #投稿一時保存テーブルを更新して投稿テーブルにデータを挿入する。
        elif request.POST['submit'] == '投稿':
            #投稿一時テーブルにデータを挿入。
            object = Post_Tmp.objects.get(post_id=postId)
            object.title = form.cleaned_data['title']
            object.tag = form.cleaned_data['tag']
            object.text_probrem = form.cleaned_data['text_probrem']
            object.text_solution = form.cleaned_data['text_solution']
            object.reference_url = form.cleaned_data['reference_url']
            object.update_timestamp = registTime
            object.already_post_fg = True
            
            object.save()#更新の反映
        
            #投稿一時テーブルの更新したデータを取得
            ptObj = Post_Tmp.objects.get(post_id=postId)
            #投稿テーブルにデータを追加
            object = Post.objects.create(
                post_id = ptObj.post_id,
                user = ptObj.user,
                title = ptObj.title,
                tag = ptObj.tag,
                text_probrem = ptObj.text_probrem,
                text_solution = ptObj.text_solution,
                reference_url = ptObj.reference_url,
                insert_timestamp = ptObj.insert_timestamp,
                update_timestamp = ptObj.update_timestamp
            )
            object.save()
        
        ctx = {"form": form, "postId": postId}
        return render(request, template_name, ctx)
        
    
    
    #POSTの場合END-----------------------------------------------------------
    #未対応のメソッド
    else:
        return HttpResponse('不正なメソッドです', status=500)
    





