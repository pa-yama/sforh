from django.views.generic import ListView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
class ListUserView(ListView):
    template_name = 'SforH/user_list.html'
    model = User
    
# ログイン後のリダイレクト用
@login_required
def index(request):
    return render(request, 'SforH/index.html', {})
