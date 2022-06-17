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
        return render(request, 'index.html', {'kandydat': kandydat})

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


@login_required(login_url='login')
def uploadfile(request):
    try:
        Upload.objects.all().delete()
        list_oc = []
        for i in Ocena.objects.all():
            list_oc.append(i.ocena)
        ocena_min = sorted(list_oc)[0]
        ocena_id=Ocena.objects.get(ocena=ocena_min)
        dir = 'media/'

        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
        # Handle file upload
        if request.method == 'POST':
            form = UploadForm(request.POST, request.FILES)
            if form.is_valid():
                docfile = Upload(file = request.FILES['docfile'])
                docfile.save()
                firstfile = Upload.objects.all()[0].file

                with open('media/' + str(firstfile), newline='') as csvfile:
                     spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                     for row in spamreader:
                           row_strip_0=row[0].strip()
                           row_strip_1 = row[1].strip()
                           row_strip_2 = row[2].strip()
                           row_strip_3 = row[3].strip()
                           row_strip_4 = row[4].strip()
                           row_strip_5 = row[5].strip()
                           row_strip_6 = str(row[6].strip())
                           user = User(password=row_strip_0,
                                       username=row_strip_1,
                                       first_name=row_strip_2,
                                       second_name=row_strip_3,
                                       last_name=row_strip_4,
                                       email=row_strip_5,
                                       pesel = row_strip_6)
                           user.save()
                           kandydat = Kandydat(
                                        user=user,
                                         j_pol_egz=0,
                                         mat_egz=0,
                                         suma_pkt=0,
                                         j_obcy_egz=0,
                                         j_pol_oc=ocena_id,
                                         mat_oc=ocena_id,
                                         biol_oc=ocena_id,
                                         inf_oc=ocena_id,
                                         )

                           kandydat.save()

                return redirect('/')
        else:
            form = UploadForm() # A empty, unbound form
    except IndexError:
        return redirect('/error/')

    # Load documents for the list page
    documents = Upload.objects.all()

    # Render list page with the documents and the form
    return render(request, 'uploadfile.html', {'documents': documents, 'form': form})
