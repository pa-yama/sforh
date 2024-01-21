from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

# パスワード変更用URLのメール送付ページ
class PasswordResetView(PasswordResetView):
    # メールタイトルの内容
    subject_template_name = 'SforH/password_reset_subject.txt'
    # メール本文の内容
    email_template_name = "SforH/password_reset_email.html"
    # パスワード変更ページ
    template_name = 'SforH/password_reset_form.html'
    # メール送信後ページ
    success_url = reverse_lazy('password_reset_done')

# パスワード変更用URLを送りましたページ
class PasswordResetDoneView(PasswordResetDoneView):
    template_name = 'SforH/password_reset_done.html'

# 新パスワード入力ページ
class PasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('SforH/password_reset_complete')
    template_name = 'SforH/password_reset_confirm.html'

# パスワード変更完了ページ
class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'SforH/password_reset_complete.html'