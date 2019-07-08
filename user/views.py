from django.shortcuts import render, HttpResponse, redirect,reverse
from django import views
from django.db import connection
import django
import re
from .forms import *
from user.models import User

# Create your views here.

class create_user(views.View):
    '''
    注册用户
    :return 注册页面
    '''
    def get(self,request):

        if request.method =='GET':
            return render(request,'register.html')
        else:
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')

            if not all([username,password,email]):
                return render(request,'register.html',{'errmsg':'数据不完整'})
            #校验邮箱
            if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

            #校验用户名是否重复

            try:
                user = User.objects.filter(username=username)
            except:
                #用户名不存在
                user = None
            if user:
                #用户名已存在
                return render(request,'register.html',{'errmsg':'用户名已存在'})

            def get(self, request):
                return render(request, 'register.html')

            def post(self, request):
                f = Register(request.POST)
                if f.is_valid():
                    f.save()
                    username = f.cleaned_data.get('username')
                    return render(request, 'register.html')
                else:
                    pwd = f.error()
                    return render(request, 'register.html', {'pwd': pwd})

