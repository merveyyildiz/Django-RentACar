from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from product.models import CommentForm,Comment


def index():
    return HttpResponse("page")

@login_required(login_url='/login') #check login
def addcomment(request,id):
    url = request.META.get("HTTP_REFERER")  # get last url yani post edilen url (yorum yazılan yer)
    if request.method == 'POST':  # form post edildiyse
        form = CommentForm(request.POST)
        if form.is_valid():  # form geçerli ise
            current_user = request.user #user bilgisini aldık
            data = Comment()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.car_id = id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR') #pc id alıyoruz
            data.save()  # veritabanına kaydet
            messages.success(request, "Yorumunuz başarı ile gönderilmişitir.Teşekkür ederiz")

            return HttpResponseRedirect(url)
    messages.warning(request, "Yorumunuz kaydedilemedi.")
    return HttpResponseRedirect(url)
