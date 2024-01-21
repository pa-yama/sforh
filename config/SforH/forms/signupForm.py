from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

User = get_user_model()

subject = "登録確認"
message_template = """
ご登録ありがとうございます。
以下URLをクリックして登録を完了してください。

"""

# 新規登録時のメール認証URL作成機能
# ユーザーidをハッシュ化してURLパラメータに追加
def get_activate_url(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return settings.FRONTEND_URL + "/activate/{}/{}/".format(uid, token)

# 新規登録form
class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    def save(self, commit=True):
        # commit=Falseだと、DBに保存されない
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        
        # 認証するまでログイン不可にする
        user.is_active = False
        
        # ユーザーを新規登録
        if commit:
            user.save()
            activate_url = get_activate_url(user)
            message = message_template + activate_url
            user.email_user(subject, message)
        return user
    
# ユーザー認証用form
def activate_user(uidb64, token):    
    # URLパラメータをデコード
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception:
        return False

    # デコードしたパラメータがユーザidと一致する場合、ユーザーをアクティベートする
    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return True
    
    return False