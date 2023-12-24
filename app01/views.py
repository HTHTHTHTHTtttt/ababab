from django.shortcuts import render

# Create your views here.
from pure_pagination import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render, redirect
from app01 import models
import random
from datetime import date
from haystack import search



def register(request):
    # 定义一个错误提示为空
    error_name = ''
    if request.method == 'POST':
        user = request.POST.get('username')
        email = request.POST.get('email')
        pwd1 = request.POST.get('pwd1')
        pwd2 = request.POST.get('pwd2')

        user_list = models.User.objects.filter(username=user)
        if user_list:
            # 注册失败
            error_name = '%s用户名已经存在了' % user
            # 返回到注册页面，并且把错误信息报出来
            return render(request, 'register.html', {'error_name': error_name})
        if pwd1 != pwd2:
            msg = '两次密码不一致'
            return render(request, 'register.html', {'msg': msg})
        else:
            # 数据保存在数据库中，并返回到登录页面
            user = models.User.objects.create(username=user,
                                              password=pwd1,
                                              email=email,
                                             )
            user.save()  # 同ip下跳转
            return redirect('/login/')
    return render(request, 'register.html')


def login(request):
    error_msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        queryset = models.User.objects.get(username=username)

        ret = models.User.objects.filter(username=username, password=password)
        if ret:
            request.session["info"]={'name':username,'id':queryset.id}
            return redirect("/buymainpage/")

        else:
            # 登录失败
            error_msg = '用户名或密码错误，请重新输入！'
            return render(request, 'login.html', {'error_msg': error_msg})
    return render(request, 'login.html')


def buymainpage(request):
    info = request.session.get("info")
    if not info:
         msg3 = '未登录'
         return render(request, "buymainpage.html", {'msg3': msg3})
    else:
        username = info["name"]
        msg1 = '欢迎用户%s' % username
        msg2 = '已登录'
        check='True'
        rep = render(request, 'buymainpage.html', {'msg1': msg1, 'MSG2': msg2,'check':check})
        return rep

def image(request):
    x=[]
    info = request.session.get("info")
    id1 = info["id"]
    if request.method=='GET':
        return render(request, 'image.html')
    if request.method=='POST':
        tp = models.Image.objects.values('id')
        for i in tp:
            x.append(list(i.values())[0])
        if id1 not in x:
            image = request.FILES.get('image')
            images = models.Image.objects.create(image=image)
            images.save()
            return render(request, 'buymainpage.html')
        else:
            msg1='你已经上传过头像了，暂不支持修改头像'
            return render(request, 'buymainpage.html', {'msg1':msg1})


def logout(request):
    del request.session['info']
    msg5 = '已登出'
    return render(request, 'buymainpage.html', {'msg5': msg5})



def search(request):
    if request.method == 'POST':
        searchinfo = request.POST.get('searchinfo')
        queryset = models.Information.objects.filter()
        p = Paginator(queryset, 3)
        page = request.GET.get('page', 1)
        try:
            queryset = p.page(int(page))
        except PageNotAnInteger:
            queryset = p.page(1)

        return render(request, 'search.html', )
    return render(request, 'search.html')






def put(request):
    x=[]
    info = request.session.get("info")
    id1 = info["id"]
    if request.method == 'GET':
        tp = models.Information.objects.values('id')
        for i in tp:
            x.append(list(i.values())[0])
        if id1 not in x:
            msg1='请先完善个人信息'
            return render(request, 'put.html', {'msg1':msg1})
        else:
            msg1='你已经放置过盲盒了'
            return render(request, 'buymainpage.html', {'msg1': msg1})


    if request.method == 'POST':

        realname = request.POST.get('realname')
        profile = request.POST.get('profile')
        tel = request.POST.get('tel')
        location = request.POST.get('location')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        qianming = request.POST.get('qianming')
        user = models.Information.objects.create(text=profile,
                                              tel=tel,
                                              age=age,
                                              gender=gender,
                                              location=location,
                                              realname=realname,
                                                 qianming=qianming)
        user.save()
        return render(request, 'buymainpage.html')

def detailshow(request,nid):
    x=[]
    info = request.session.get("info")
    username = info["name"]
    tpname = models.History.objects.filter(username=username)
    tp = tpname.values('hid')

    for i in tp:
        x.append(list(i.values())[0])
    if nid not in x:
        historys = models.History.objects.create(hid=nid, username=username)
        historys.save()
    queryset = models.Information.objects.filter(id=nid)
    images = models.Image.objects.filter(id=nid)
    comquery = models.Comment.objects.filter(nid=nid)
    recomquery = models.ReComment.objects.all()
    return render(request, 'detailshow.html', {'images': images, 'queryset': queryset,
                                               'comquery': comquery,'username':username,'recomquery':recomquery})

def suiji(request):
    x = []
    tp = models.Information.objects.values('id')
    info = request.session.get("info")
    username = info["name"]
    for i in tp:
        x.append(list(i.values())[0])
    rannum=random.randint(0,len(x)-1)
    number=x[rannum]
    queryset = models.Information.objects.filter(id=number)
    images = models.Image.objects.filter(id=number)
    comquery = models.Comment.objects.filter(nid=number)
    recomquery = models.ReComment.objects.all()
    return render(request, 'randetailshow.html', {'images': images, 'queryset': queryset,
                                               'comquery': comquery,'username':username,'recomquery':recomquery})


def next(request,nid):
    nid1=nid+1
    return detailshow(request,nid=nid1)

def last(request,nid):
    nid1=nid-1
    return detailshow(request,nid=nid1)

def comment(request,nid):
    if request.method == 'GET':
        return render(request, 'comment.html')
    if request.method == 'POST':
        info = request.session.get("info")
        com=request.POST.get('comment')
        username=info["name"]
        time=date.today()
        comments=models.Comment.objects.create(com=com,username=username,time=time,nid=nid)
        comments.save()
        return render(request, 'buymainpage.html')

def delete(request,nid):
    models.Comment.objects.filter(id=nid).delete()
    return render(request, 'buymainpage.html')

def history(request):
    info = request.session.get("info")
    username = info["name"]
    hiqueryset=models.History.objects.filter(username=username)
    queryset=models.Information.objects.all()
    return render(request, "history.html",{'queryset':queryset,'hiqueryset':hiqueryset} )


def myinformation(request):
    info = request.session.get("info")
    id1 = info["id"]
    return detailshow(request,id1)

def houtai(request):
    if request.method == 'GET':
        return render(request, 'houtaidenglu.html')
    if request.method == 'POST':
        queryset = models.Information.objects.all()
        password = request.POST.get('password')
        if password=="123":
            return render(request, 'houtai.html', {'queryset': queryset})
        else:
            msg1='管理员密码错误'
            return render(request, 'buymainpage.html', {'msg1': msg1})

def guandelete(request,nid):
    models.Information.objects.filter(id=nid).delete()
    return render(request, 'buymainpage.html')

def recomment(request,nid):
    if request.method == 'GET':
        return render(request, 'recomment.html')
    if request.method == 'POST':
        info = request.session.get("info")
        com = request.POST.get('comment')
        username = info["name"]
        time = date.today()
        comments = models.ReComment.objects.create(com=com, username=username, time=time, nid=nid)
        comments.save()
        return render(request, 'buymainpage.html')
def welcome(request):
    return render(request, 'welcome.html')
