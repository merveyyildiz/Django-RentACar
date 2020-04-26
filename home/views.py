from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import json
# Create your views here.
from home.models import Setting, ContactFormu, ContactFormMessage
from product.models import Car, Category, Images, Comment
from home.forms import SearchForm, SignUpForm


def index(request):  # home daki urls.py den çağrılıyor
    setting = Setting.objects.get(pk=1)
    sliderdata = Car.objects.all()[:4]  # ilk dört veriyi al
    category = Category.objects.all()  # tüm kategor alıyruz
    dayproducts = Car.objects.all()[:3]
    lastproducts = Car.objects.all().order_by('-id')[:3]
    randomproducts = Car.objects.all().order_by('?')[:4]
    context = {'setting': setting, 'page': 'home', 'sliderdata': sliderdata,
               'category': category,
               'dayproducts': dayproducts,
               'lastproducts': lastproducts,
               'randomproducts': randomproducts}  # içeriğe yükleyeceğimiz veriler
    return render(request, 'index.html', context)


def hakkimizda(request):  # ana urls.py den çağırılıyor
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()  # tüm kategor alıyruz
    context = {'setting': setting, 'category': category}
    return render(request, 'hakkimizda.html', context)


def referanslarimiz(request):  # ana urls.py den çağırılıyor
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()  # tüm kategor alıyruz
    context = {'setting': setting, 'category': category}
    return render(request, 'referanslarimiz.html', context)


def iletisim(request):  # ana urls.py den çağırılıyor
    # kaydetme şekli
    if request.method == 'POST':  # form post edildiyse
        form = ContactFormu(request.POST)
        if form.is_valid():  # form geçerli ise
            data = ContactFormMessage()  # model ile bağlantı kur
            data.name = form.cleaned_data['name']  # bilgiyi al
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # veritabanına kaydet
            messages.success(request, "Mesajınız başarı ile gönderilmişitir.")
            return HttpResponseRedirect('/iletisim')
        # bu kısım forma ulaşmak için
    setting = Setting.objects.get(pk=1)
    form = ContactFormu
    category = Category.objects.all()  # tüm kategor alıyruz
    context = {'setting': setting, 'form': form,
               'category': category}  # setting ve form iletişim sayfasına göndereceğiz
    return render(request, 'iletisim.html', context)


def category_products(request, id, slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    products = Car.objects.filter(category_id=id)
    context = {'products': products, 'category': category, 'categorydata': categorydata}
    return render(request, 'car.html', context)


def product_detail(request, id, slug):
    category = Category.objects.all()
    product = Car.objects.get(pk=id)
    images = Images.objects.filter(car_id=id)  # galeri için
    comments = Comment.objects.filter(car_id=id, status='True')
    context = {'category': category, 'product': product, 'images': images, 'comments': comments}
    return render(request, 'car_detail.html', context)


def product_search(request):  # ana urls.py den çağırılıyor
    # kaydetme şekli
    if request.method == 'POST':  # form post edildiyse
        form = SearchForm(request.POST)
        if form.is_valid():  # form geçerli ise
            category = Category.objects.all()
            query = form.cleaned_data['query']  # bilgiyi al
            product = Car.objects.filter(
                title__icontains=query)  # contains içermek başına i yazarsak büyük küçük harf farketmez
            context = {'product': product, 'category': category}  # setting ve form iletişim sayfasına göndereceğiz
            return render(request, 'car_search.html', context)
    return HttpResponseRedirect('/')


def product_search_auto(request):  # arama yapmak için
    if request.is_ajax():
        q = request.GET.get('term', '')
        car = Car.objects.filter(title__icontains=q)
        results = []
        for rs in car:
            car_json = {}
            car_json = rs.title
            results.append(car_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.error(request, "Login Hatası. Kullanıcı adı veya şifre yanlış")
            return HttpResponseRedirect('/login')
    category = Category.objects.all()
    context = {'category': category}
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/')

        else:
            messages.error(request, "Hata. ")
            return HttpResponseRedirect('/signup')
    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category, 'form': form}
    return render(request, 'signup.html', context)
