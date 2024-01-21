from django.shortcuts import render

def react_app(request):
    ctx = {}
    return render(request, 'index.html', ctx)

