from django.shortcuts import render, reverse
from django.views import View
from .forms import UserLoginForm
from django.http import HttpResponseRedirect, HttpResponse, Http404


# Create your views here.
def login(request):
    if request.method == 'GET':
        template_name = 'user/login.html'
        context = {}
        return render(request, template_name, context)
