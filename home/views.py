from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting, ContactFormu, ContactFormMessage


def index(request): #home daki urls.py den çağrılıyor
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page': 'home'} #içeriğe yükleyeceğimiz veriler
    return render(request, 'index.html', context)


def hakkimizda(request):#ana urls.py den çağırılıyor
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'hakkimizda.html', context)


def referanslarimiz(request):#ana urls.py den çağırılıyor
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'referanslarimiz.html', context)


def iletisim(request): #ana urls.py den çağırılıyor
    #kaydetme şekli
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
        #bu kısım forma ulaşmak için
    setting = Setting.objects.get(pk=1)
    form = ContactFormu
    context = {'setting': setting, 'form': form}  # setting ve form iletişim sayfasına göndereceğiz
    return render(request, 'iletisim.html', context)
