from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from product.models import Comment
# Create your views here.
from home.models import UserProfile
from product.models import Category
from user.forms import UserUpdateForm, ProfileUpdateForm


def index(request):
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'category': category, 'profile': profile}
    return render(request, 'user_profile.html', context)


def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)  # user ile ilişki kur
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Bilgileriniz Güncellendi')
            return redirect('/user')

    else:
        category = Category.objects.all()
        current_user = request.user
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(
            instance=request.user.userprofile)  # user ile userprofile onetoone ilişkisi kuruyor

        context = {
            'category': category, 'user_form': user_form, 'profile_form': profile_form
        }
        return render(request, 'user_update.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Şifreniz değiştirildi")
            return HttpResponseRedirect("/user")

        else:
            messages.error(request, "Tekrar deneyin<br>" + str(form.errors))
            return HttpResponseRedirect("/user/password")
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)  # bu model zaten djangoda var biz oluşturmuyotuz
        return render(request, "change_password.html", {
            'form': form, 'category': category
        })

@login_required(login_url='/login')
def comments(request):
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'category': category, 'comments': comments,
    }
    return render(request, "user_comments.html", context)

@login_required(login_url='/login')
def deletecomment(request,id):
    current_user = request.user
    comments = Comment.objects.filter(id=id,user_id=current_user.id).delete()
    messages.success(request, "Yorum silindi")
    return HttpResponseRedirect('/user/comments')