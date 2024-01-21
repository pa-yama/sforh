from django.views.generic import ListView
from ..models import User


# Create your views here.
class ListUserView(ListView):
    template_name = 'SforH/user_list.html'
    model = User