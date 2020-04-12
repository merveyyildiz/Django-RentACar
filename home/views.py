from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting, ContactFormu, ContactFormMessage
from product.models import Car, Category


def index(request):  # home daki urls.py den çağrılıyor
    setting = Setting.objects.get(pk=1)
    sliderdata = Car.objects.all()[:4]  # ilk dört veriyi al
    category = Category.objects.all()  # tüm kategor alıyruz
    dayproducts=Car.objects.all()[:3]
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
    context = {'setting': setting}
    return render(request, 'hakkimizda.html', context)


def referanslarimiz(request):  # ana urls.py den çağırılıyor
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
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
    context = {'setting': setting, 'form': form}  # setting ve form iletişim sayfasına göndereceğiz
    return render(request, 'iletisim.html', context)


def category_products(request, id, slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    products = Car.objects.filter(category_id=id)
    context = {'products': products, 'category': category,'categorydata': categorydata}
    return render(request, 'car.html', context)
