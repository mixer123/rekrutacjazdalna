import csv

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.urls import reverse
from django.views import generic
from .forms import *

from .models import *
from django.db.models import Count
from django.shortcuts import redirect

# from .models import Upload
from .forms import KandydatForm
from django.shortcuts import render
# Create your views here.
import os


def starting_page(request):
    if request.user.is_authenticated:

        print('user', request.user)
    else:
        pass
    return render(request, 'index.html')


@login_required(login_url='/accounts/login')
def chooseclas(request):
    all_klas = Klasa.objects.all()

    return render(request, 'chooseclas.html', {'all_klas': all_klas})


@login_required(login_url='/accounts/login')
def zapisz(request):
    patern = request.user
    user = User.objects.get(username=patern)
    clas = Klasa.objects.get(name=request.GET['klass'])
    user = get_object_or_404(User, pk=user.id)
    if Kandydat.objects.filter(user_id=user.id).exists() == False:
        user = Kandydat(user_id=user.id, clas_id=clas.id)
        user.save()
    return render(request, 'zapisz.html')


@login_required(login_url='/accounts/login')
def zmienlogin(request):
    patern = request.user
    user1 = User.objects.get(username=patern)
    user = get_object_or_404(User, id=user1.id)

    form = UserForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return render(request, 'success.html')

    return render(request, 'zmienlogin.html', {'user': user, 'form': form})



@login_required(login_url='/accounts/login')
def zmienclas(request):
    patern = request.user
    user = User.objects.get(username=patern)
    kandydat = get_object_or_404(Kandydat, user_id=user.id)

        # pass the object as instance in form
    form = KandydatForm(request.POST or None, instance=kandydat)

    if form.is_valid():
        form.save()
        return render(request, 'success.html')

    return render(request, 'zmienclas.html', {'user': user, 'form': form})

