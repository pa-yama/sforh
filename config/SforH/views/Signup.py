from django.urls import reverse_lazy
from ..forms.signupForm import SignupForm
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from ..forms.signupForm import activate_user


# 新規登録ページ
class SignUpView(CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('login')
    template_name = 'SforH/signup.html'

# User認証ページ
class ActivateView(TemplateView):
    template_name = "SforH/activate.html"
    
    def get(self, request, uidb64, token, *args, **kwargs):
        # 認証トークンを検証して、
        result = activate_user(uidb64, token)
        # コンテクストのresultにTrue/Falseの結果を渡す
        return super().get(request, result=result, **kwargs)