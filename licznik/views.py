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
        patern = request.user
        user = User.objects.get(username=patern)
        kandydat = Kandydat(user_id=user.id)
    else:
        pass
    return render(request, 'index.html',{'kandydat':kandydat})


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



@login_required(login_url='login-page')
def zestawienieklasy(request):
    clas = Klasa.objects.get(name=request.GET['klass'])
    doc_oryg = get_object_or_404(Oryginal, name='ORYGINAL')
    doc_kopia = get_object_or_404(Oryginal, name='KOPIA')
    doc_podanie = get_object_or_404(Oryginal, name='PODANIE')
    kand_oryg = Kandydat.objects.filter(clas=clas,document=doc_oryg).values('user__last_name','user__first_name','user__pesel')\
        .order_by('-document__name','user__last_name')
    kand_oryg_il = kand_oryg.count()
    kand_kopia = Kandydat.objects.filter(clas=clas, document=doc_kopia).values('user__last_name', 'user__first_name',
                                                                             'user__pesel') \
        .order_by('-document__name', 'user__last_name')
    kand_kopia_il = kand_kopia.count()
    kand_podanie = Kandydat.objects.filter(clas=clas, document=doc_podanie).values('user__last_name', 'user__first_name',
                                                                             'user__pesel') \
        .order_by('-document__name', 'user__last_name')
    kand_podanie_il = kand_podanie.count()
    return render(request, 'zestawienieklasy.html', {'kand_oryg':kand_oryg,'kand_kopia':kand_kopia,'kand_podanie':kand_podanie,
                                                     'clas':clas,'kand_oryg_il':kand_oryg_il,
                                                     'kand_kopia_il':kand_kopia_il, 'kand_podanie_il':kand_podanie_il})

@login_required(login_url='login-page')
def zestawienie(request):
    all_klas = Klasa.objects.all()
    return render(request, 'zestawienie.html',{'all_klas': all_klas})

