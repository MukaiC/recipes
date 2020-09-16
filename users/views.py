from django.shortcuts import render

def register(request):
    return render(request, 'users/register.html')

def login_view(request):
    return render(request, 'users/login.html')
