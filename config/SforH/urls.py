from django.urls import path

from .views import PasswordReset, Signup, UtilViews
from django.urls import path, include
from .views import listUserView, ReactViews, createPostReact, searchPostList, detail, sendReact, detailReact
from .views import listUserView, createPost, searchPostList, detail, sendReact, detailReact, header



urlpatterns = [
    #path('', UtilViews.ListUserView.as_view()),# SforH/ = user_list.htmlのパス
    #path('index', ReactViews.react_app, name='index'),
    #path('index', UtilViews.index, name='index'),# ログイン後のリダイレクト用（一覧画面ができれば削除）
    path('', UtilViews.ListUserView.as_view()),# SforH/ = user_list.htmlのパス
    path('index', UtilViews.index, name='index'),# ログイン後のリダイレクト用
    path('signup/', Signup.SignUpView.as_view(), name='signup'),# 新規登録用
    path('activate/<uidb64>/<token>/', Signup.ActivateView.as_view(), name='activate'),# 新規登録認証用URL
    path('password_reset/', PasswordReset.PasswordResetView.as_view(), name='password_reset'),# パスワード再設定メール送信画面
    path('password_reset/done/', PasswordReset.PasswordResetDoneView.as_view(), name='password_reset_done'),# パスワード再設定メール完了画面
    path('reset/<uidb64>/<token>/', PasswordReset.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),# パスワード再設定認証画面
    path('reset/done/', PasswordReset.PasswordResetCompleteView.as_view(), name='password_reset_complete'),# パスワード再設定認証完了画面
    path('', include('django.contrib.auth.urls')),# 認証機能の各画面

    #ヘッダー用
    path('header/', header.getSession, name="header"),
    
    #path('SforH/', Saveviews.ListUserView.as_view(), name='user-list'),#SforH/ = user_list.htmlのパス
    
    #path('SforH/createPost/', createPostFunc.createPostFunc, name='create-post'),#SforH/createPost/ = createPost.htmlのパス
    
    path('post/', searchPostList.searchPostList, name='search-post'),#SforH/ = search_post.htmlのパス
    #path('test2/', searchPostList.test2.as_view({'get': 'list'}), name="data-list"),
    path('searchPost/', searchPostList.searchPost, name="search"),
    path('test3/', searchPostList.test3.as_view(), name="datail-data"),
    #path('SforH/detail/', detailFunc.detailFunc, name='detail'),#SforH/createPost/ = detail.htmlのパス
    
    
    #sendReact
    path('sendReact/', sendReact.sendReact, name="sendReact"),
    
    #path('SforH/detail/<post_id>/', detailFunc.detailFunc, name='detail'),#SforH/createPost/ = detail.htmlのパス
    
    #createPost関連のパス
    #ヘッダーから遷移
    #path('createPost/', createPostReact.fromHeaderFunc, name='create-post'),#SforH/createPost/ = createPost.htmlのパス
    #詳細画面から遷移
    #path('createPost/edit/', createPostReact.fromDetailFunc, name='create-post-edit'),#SforH/createPost/ = createPost.htmlのパス
    #一時保存リストから遷移
    #path('createPost/tmpList/', createPostReact.fromTmpListFunc, name='create-post-tmpList'),#SforH/createPost/ = createPost.htmlのパス
    
    
    #createPost関連のパス
    path('createPost/', createPostReact.fromHeaderFunc, name='create-post'),#SforH/createPost/ = createPost.htmlのパス
    path('createPost/create/', createPostReact.fromHeaderCreatePostFunc, name='createPost'),#SforH/createPost/ = createPost.htmlのパス
    path('createPost/save/', createPostReact.fromHeaderSavePostFunc, name='savePost'),#SforH/createPost/ = createPost.htmlのパス
    
    #詳細画面から遷移
    path('createPost/edit/<post_id>/', createPostReact.fromDetailFunc, name='create-post-edit'),#SforH/createPost/ = createPost.htmlのパス
    path('createPost/edit/<post_id>/create/', createPostReact.fromDetailCreatePostFunc, name='createPost-edit'),#SforH/createPost/ = createPost.htmlのパス
    path('createPost/edit/<post_id>/save/', createPostReact.fromDetailSavePostFunc, name='savePost-edit'),#SforH/createPost/ = createPost.htmlのパス
    
    #一時保存リストから遷移
    path('createPost/tmpEdit/<post_id>/', createPostReact.fromTmpListFunc, name='create-post-tmpList'),#SforH/createPost/ = createPost.htmlのパス
    
    
    
    
    
    #detail関連のパス
    #初期表示時
    #path('detail/<post_id>/', detail.detailFunc, name='detail'),#SforH/createPost/ = detail.htmlのパス
    path('detail/<post_id>/', detailReact.detailFunc, name='detail'),#SforH/createPost/ = detail.htmlのパス
    #コメント投稿処理
    path('detail/<post_id>/comment/', detailReact.detailCommentFunc, name='detail-comment'),#SforH/createPost/ = detail.htmlのパス
    #コメント返信処理
    path('detail/<post_id>/reply/', detailReact.detailReplyFunc, name='detail-reply'),#SforH/createPost/ = detail.htmlのパス
    #返信コメントに返信の処理
    path('detail/<post_id>/replyToReply/', detailReact.detailReplyToReplyFunc, name='detail-reply'),#SforH/createPost/ = detail.htmlのパス
    
    
    #投稿にいいね
    path('detail/<post_id>/goodPost/', detailReact.detailGoodPostFunc, name='detail-goodPost'),#SforH/createPost/ = detail.htmlのパス
    #コメントにいいね
    path('detail/<post_id>/goodComment/', detailReact.detailGoodCommentFunc, name='detail-goodComment'),#SforH/createPost/ = detail.htmlのパス
    
    #投稿にいいね解除
    path('detail/<post_id>/unlikePost/', detailReact.detailUnlikePostFunc, name='detail-unlikePost'),#SforH/createPost/ = detail.htmlのパス
    #コメントにいいね
    path('detail/<post_id>/unlikeComment/', detailReact.detailUnlikeCommentFunc, name='detail-unlikeComment'),#SforH/createPost/ = detail.htmlのパス
    
    
]