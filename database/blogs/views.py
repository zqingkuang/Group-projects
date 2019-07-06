from PIL import Image, ImageDraw, ImageFont
from django.utils.six import BytesIO
from django.shortcuts import HttpResponse, render, redirect
from .models import *
from .forms import *
from django import views


# /verify_code
def verify_code(request):
    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象，字体路径为”booktest/FreeMono.ttf”
    font = ImageFont.truetype('FreeMono.ttf', 23)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    print(rand_str)
    # 内存文件操作
    buf = BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    de = buf.getvalue()
    return HttpResponse(de, 'image/png')


def index(request):
    """
    首页显示 \n
    :param request:
    :return:
    """
    b = ThumbsUp.objects.all()
    a = ArticleModel.objects.all()
    return render(request, 'index.html', {'a': a, 'b': b})


class register(views.View):
    """
    注册 \n
    """

    def get(self, request):
        """
        获取注册页面 \n
        :param request:
        :return:
        """
        return render(request, "zhuce.html")

    def post(self, request):
        """
        获取注册信息 \n
        :param request:
        :return:
        """
        # 获取用户输入的验证码
        vcode_input = request.POST.get('vcode')
        # 获取session中存储的验证码
        vcode_session = request.session.get('verifycode')
        # 进行验证码的校验
        if vcode_input != vcode_session:
            # 验证码错误

            return render(request, 'zhuce.html', {'a': '验证码错误'})

        f = LoginForm(request.POST)
        if f.is_valid():
            username = f.cleaned_data.get('username')
            print(username)
            password = f.cleaned_data.get('password')
            print(password)
            name = request.POST.get("name")
            print(name)
            age = request.POST.get("age")
            print(age)
            phone = request.POST.get('phone')
            print(phone)
            sign = request.POST.get("sign")
            print(sign)
            sex = request.POST.get("sex")
            print(sex)
            s = UserModel.objects.create(username=username, password=password, name=name, age=age, phone=phone,
                                         sign=sign, sex=sex, this_g_id=1)

            return redirect('index')  # 跳转登陆页面

        else:
            d = f.errors.get_json_data()
            print(d)
            e = []
            for i in d.keys():
                e.append(i)
            print(e)
            b = []
            for i in d[e[0]][0].keys():
                b.append(i)
            print(b)
            print(d[e[0]][0][b[0]])
            if e[0] == 'phone':
                return render(request, 'zhuce.html', {'c': d[e[0]][0][b[0]]})
            return render(request, 'zhuce.html', {'b': d[e[0]][0][b[0]]})


class LIndex(views.View):
    """
    登陆 \n
    """

    def get(self, request):
        """
        获取登陆页面 \n
        :param request:
        :return:
        """
        return render(request, "register.html")

    def post(self, request):
        """
        获取登陆信息 \n
        :param request:
        :return:
        """
        # 获取用户输入的验证码
        vcode_input = request.POST.get('vcode')
        # 获取session中存储的验证码
        vcode_session = request.session.get('verifycode')
        # 进行验证码的校验
        if vcode_input != vcode_session:
            # 验证码错误

            return render(request, 'register.html', {'a': '验证码错误'})
        u_name = request.POST.get("username")
        u_card = request.POST.get("password")
        try:
            b = UserModel.objects.get(username=u_name, password=u_card)
        except:
            return render(request, 'register.html', {'b': "用户名或密码错误"})
        else:
            request.session["u_id"] = b.id
            return redirect("index")  # 跳转页面


def de(request, sd):
    """
    跳转条件页面
    :param request:
    :param sd:
    :return:
    """
    return render(request, sd)


def per_home(request):
    """
    个人主页
    :param request:
    :return:
    """
    u_id = request.session.get("u_id")
    if u_id:

        if request.method == 'GET':
            d = UserModel.objects.get(id=u_id)
            return render(request, 'main.html', {'d': d})

        else:
            username = request.POST.get('username')
            password = request.POST.get('password')
            name = request.POST.get('name')
            age = request.POST.get('age')
            head = request.POST.get('head')
            sign = request.POST.get('sign')
            sex = request.POST.get('sex')
            s = UserModel.objects.get(pk=u_id)
            s.username = username
            s.password = password
            s.name = name
            s.age = age
            s.head = head
            s.sign = sign
            s.sex = sex

            s.save()
            return redirect('index')  # 跳转个人主页



    else:
        return render(request, 'register.html')


def write_ArticleModel(request):
    '''
    添加文章
    :param request:
    :return:
    '''
    u_id = request.session.get("u_id")
    if u_id:
        if request.method == 'GET':
            return render(request, 'write_article.html')
        else:
            title = request.POST.get('title')  # 获取文章名
            content = request.POST.get('content')  # 获取文章内容
            user_s = u_id  # 获取用户外键
            # file = request.POST.get('file')  # 获取文件
            s = ArticleModel(title=title, content=content, user_s_id=user_s)
            s.save()
            return redirect('index')
    else:
        return render(request, 'register.html')


def del_ArticleModel(request, sid):
    '''
    删除文章
    :param request:sid
    :return:
    '''
    sid = ArticleModel.objects.get(pk=sid)
    sid.delete()
    return redirect('index')


# def phone_password(request):
#     '''
#     修改密码
#     '''
#     u_id = request.session.get("u_id")
#     if u_id:
#         if request.method == 'GET':
#             return render(request, 'retrieve_password.html')
#         else:
#             rp = loginForm(request.POST)
#             if rp.is_valid():
#                 username = rp.cleaned_data.get('username')
#                 password = rp.cleaned_data.get('password')
#                 username.objects.filter(username=username).update(password=password)
#                 return redirect('login')
#             else:
#                 e = rp.error()
#                 return render(request, 'retrieve_password.html', {'e': e})
#     else:
#         return render(request, 'register.html')


def flush(request):
    """
    注销登录
    :param request:
    :return:
    """
    request.session.flush()
    return redirect('index')


def thumbsup(request, sid):
    """
    点赞效果
    :param request:
    :return:
    """
    u_id = request.session.get("u_id")
    if u_id:
        try:
            s = ThumbsUp.objects.get(this_u_id=u_id, this_a_id=sid)
        except:
            ThumbsUp.objects.create(this_u_id=u_id, this_a_id=sid)
            return redirect('index')
        else:
            s.delete()
            return redirect('index')
    else:
        return render(request, 'register.html')


def repyle1(request, id):
    """
    记录评论
    :param request:
    :param id:
    :param sid:
    :return:
    """
    u_id = request.session.get("u_id")
    if u_id:
        r = request.POST.get('shuru')
        CommentModel.objects.create(content=r, this_a_id=id, this_u_id=u_id, )
        return redirect('index')
    else:
        return render(request, 'register.html')


def pinglun(request, sid):
    """
    跳转评论
    :param request:
    :param sid:
    :return:
    """

    s = ArticleModel.objects.get(id=sid)

    return render(request, 'pinglun.html', {'s': s})


def guanzhu(request, sid):
    """
    记录关注人
    :param request:
    :return:
    """
    u_id = request.session.get("u_id")
    try:
        a = Attention.objects.get(att_u1_id=u_id, att_u2_id=sid)
    except:
        d = Attention.objects.create(att_u1_id=u_id, att_u2_id=sid)
        return redirect('guan')
    else:
        a.delete()
        return redirect('guan')


def guan(request):
    """
    跳转关注页面
    :param request:
    :return:
    """
    u_id = request.session.get("u_id")
    if u_id:

        d = UserModel.objects.all()
        s = Attention.objects.filter(att_u1_id=u_id)
        return render(request, 'guanzhu.html', {'d': d, 's': s})
    else:
        return render(request, 'register.html')


def renyuan(request):
    """
    好友页面
    :param request:
    :return:
    """
    u_id = request.session.get("u_id")
    if u_id:
        s = Attention.objects.filter(att_u1_id=u_id)
        return render(request, 'renyuan.html', {'s': s})
    else:
        return render(request, 'register.html')


def dd(request, sid):
    """
    查看好友信息
    :param request:
    :return:
    """
    a = UserModel.objects.get(id=sid)
    return render(request, 'main1.html', {'d': a})


def wenzhang(request):
    """
    查看个人发布文章
    :param request:
    :return:
    """
    u_id = request.session.get("u_id")
    if u_id:
        a = ArticleModel.objects.filter(user_s_id=u_id)
        return render(request, 'wenzhang.html', {'a': a})
    else:
        return render(request, 'register.html')


def haoyou(request):
    """
    查看关注人的文章
    :param request:
    :return:
    """
    u_id = request.session.get("u_id")
    if u_id:
        a = Attention.objects.filter(att_u1_id=u_id)
        return render(request, 'haoyou.html', {'a': a})

    else:
        return render(request, 'register.html')


def chazhao(request):
    """
    查找标题的文章内容
    :param request:
    :return:
    """
    s = request.POST.get('q')
    c = ArticleModel.objects.filter(title__icontains=s)
    b = ArticleModel.objects.filter(title=s)
    a = (c | b).distinct()

    print(a,b,c)
    return render(request, 'chazhao.html', {'a': a})
