from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.urls import reverse

def user_logout(request):
    auth_logout(request)
    return redirect(reverse('user:login'))