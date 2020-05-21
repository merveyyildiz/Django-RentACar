from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import logging
logger = logging.getLogger(__name__)
import json
from django.utils.crypto import get_random_string
# Create your views here.
from home.models import Setting, ContactFormu, ContactFormMessage, UserProfile, OrderForm, Order, OrderProduct, \
    CalculateForm, Calculate, Faq
from product.models import Car, Category, Images, Comment
from home.forms import SearchForm, SignUpForm


def index(request):  # home daki urls.py den çağrılıyor
    setting = Setting.objects.get(pk=1)
    sliderdata = Car.objects.all()[:4]  # ilk dört veriyi al
    category = Category.objects.all()  # tüm kategor alıyruz
    dayproducts = Car.objects.filter(status="True")[:3]
    lastproducts = Car.objects.filter(status="True").order_by('-id')[:3]
    randomproducts = Car.objects.filter(status="True").order_by('?')[:4]
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
    setting = Setting.objects.get(pk=1)
    categorydata = Category.objects.get(pk=id)
    products = Car.objects.filter(category_id=id, status="True")
    context = {'products': products, 'category': category, 'categorydata': categorydata, 'setting': setting}
    return render(request, 'car.html', context)


def product_detail(request, id, slug):
    category = Category.objects.all()
    product = Car.objects.get(pk=id)
    setting = Setting.objects.get(pk=1)
    images = Images.objects.filter(car_id=id)  # galeri için
    if request.method == 'POST':
        form = CalculateForm(request.POST)
        if form.is_valid():  # form geçerli ise
            data = Calculate()
            date_start=(form.cleaned_data['date_start']).date()
            date_end=(form.cleaned_data['date_end']).date()
            day=(date_end-date_start).days
            logger.info("The value of var is %s", day)
            data.date_start = date_start
            data.date_end =date_end
            data.day = day
            data.save()
            return HttpResponseRedirect("/order/orderproduct/%s" % product.id)
    comments = Comment.objects.filter(car_id=id, status='True')
    context = {'category': category, 'product': product, 'images': images, 'comments': comments, 'setting': setting}
    return render(request, 'car_detail.html', context)


def product_search(request):  # ana urls.py den çağırılıyor
    # kaydetme şekli
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':  # form post edildiyse
        form = SearchForm(request.POST)
        if form.is_valid():  # form geçerli ise
            category = Category.objects.all()
            query = form.cleaned_data['query']  # bilgiyi al
            product = Car.objects.filter(
                title__icontains=query)  # contains içermek başına i yazarsak büyük küçük harf farketmez
            context = {'product': product, 'category': category,
                       'setting': setting}  # setting ve form iletişim sayfasına göndereceğiz
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
    setting = Setting.objects.get(pk=1)
    context = {'category': category, 'setting': setting}
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
            current_user = request.user
            data = UserProfile() #kişi kayıt olduğunda otomatik profile oluşturmak için
            data.user_id = current_user.id
            data.image = "images/user.jpg"
            data.phone = 123456789
            data.save()
            messages.success(request, "Sisteme başarılı bir şekilde kaydoldunuz")
            return HttpResponseRedirect('/')

        else:
            messages.error(request, "Hata. ")
            return HttpResponseRedirect('/signup')
    form = SignUpForm()
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'category': category, 'form': form, 'setting': setting}
    return render(request, 'signup.html', context)


@login_required(login_url='/login')  # check login
def orderproduct(request, id):#rezervasyon
    url = request.META.get("HTTP_REFERER")  # gelinen url
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    product = Car.objects.get(id=id)
    total = Calculate.objects.all().order_by('-id')[0].day * product.price
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():  # form geçerli ise
            data = Order()
            data.first_name = form.cleaned_data['first_name']  # formdan veriyi getiriyor
            data.last_name = form.cleaned_data['last_name']  # formdan veriyi getiriyor
            data.city = form.cleaned_data['city']  # formdan veriyi getiriyor
            data.phone = form.cleaned_data['phone']  # formdan veriyi getiriyor
            data.date_start = Calculate.objects.all().order_by('-id')[0].date_start
            data.date_end = Calculate.objects.all().order_by('-id')[0].date_end
            data.quatity = Calculate.objects.all().order_by('-id')[0].day
            data.address = form.cleaned_data['address']
            data.country = form.cleaned_data['country']
            data.user_id = current_user.id
            data.car_id = id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()
            data.code = ordercode
            data.save()

            orderproduct = OrderProduct()
            orderproduct.user_id = current_user.id
            product.amount = product.amount - 1
            product.save()
            Calculate.objects.all().order_by('-id')[0].delete()
            messages.success(request, "Rezervasyonunuz Yapıldı\nCode %s" % ordercode)
            return HttpResponseRedirect(url)
            # return HttpResponseRedirect("/")
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect(url)
    form = OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'category': category,
               'total': total,
               'form': form,
               'profile': profile,
               'setting': setting
               }
    return render(request, 'Order_Form.html', context)


def faq(request):#sss
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    faq = Faq.objects.all().order_by('ordernmbr')
    context = {'category': category, 'setting': setting, 'faq': faq}
    return render(request, 'faq.html', context)

