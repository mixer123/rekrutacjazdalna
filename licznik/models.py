from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator

# Create your models here.
from django.http import request

from rekrutacjazdalna2022 import settings


class User(AbstractUser):
    pesel = models.CharField(max_length=10, unique=True)
    second_name = models.CharField(null=True, blank=True, max_length=10)





class Klasa(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='')
    class Meta:
        verbose_name_plural = "Klasa"
        verbose_name = "Klasa"

    def __str__(self):
        return self.name

    def save(self):
        self.name = self.name.upper()
        super(Klasa, self).save()

class Oryginal(models.Model):
    name = models.CharField(max_length=100, unique=True , verbose_name='')
    class Meta:
        verbose_name_plural = "Dokumenty"
        verbose_name = "Dokumenty"

    def __str__(self):
        return self.name

    def save(self):
        self.name = self.name.upper()
        super(Oryginal, self).save()

class Ocena(models.Model):
    class Meta:
        verbose_name_plural = "Oceny"
        verbose_name = "Oceny"
    OCENY = (
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
    )
    ocena = models.IntegerField(default=2,  unique=True, choices=OCENY)
    punkty = models.IntegerField(default=2)

    def __str__(self):
        return f'{str(self.ocena)}, {str(self.punkty)}'


class Kandydat(models.Model):
    class Meta:
        verbose_name_plural = "Kandydat"
        verbose_name = "Kandydat"
    # Konkursy ponad wojewódzkie
    KPW = (
        (0,0),
        (5, 5),
        (7, 7),
        (10, 10),
    )

    # Konkursy przedmiotowy
    KP = (
        (0, 0),
        (3, 3),
        (4, 4),
        (10, 10),
    )

    # Konkursy wojewódzkie
    KW = (
        (0, 0),
        (3, 3),
        (5, 5),
        (7, 7),
        (10, 10),
    )
#Konkursy inne
    KI = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
    )
    # Aktywność społeczna
    AS = (
    (0, 0),
    (3, 3),
)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    clas =  models.ForeignKey(Klasa, null=True, on_delete=models.SET_NULL, verbose_name='Klasa')
    document  = models.ForeignKey(Oryginal, null=True, on_delete=models.SET_NULL, verbose_name='Dokument')
    internat = models.BooleanField(default=False, verbose_name='Internat')
    j_pol_egz = models.IntegerField(default=0, verbose_name='J.polski punkty egzamin',validators=[
            MaxValueValidator(50),MinValueValidator(0)])
    mat_egz = models.IntegerField(default=0, verbose_name='Matematyka punkty egzamin',validators=[
            MaxValueValidator(50),MinValueValidator(0)])
    j_obcy_egz = models.IntegerField(default=0, verbose_name='J.obcy punkty egzamin',validators=[
            MaxValueValidator(50),MinValueValidator(0)])
    j_pol_oc = models.ForeignKey(Ocena, null=True,  on_delete=models.SET_NULL, related_name='j_pol_oc', verbose_name='J.polski ocena')
    mat_oc = models.ForeignKey(Ocena, null=True, on_delete=models.SET_NULL, related_name='mat_oc',  verbose_name='Matematyka ocena')
    biol_oc = models.ForeignKey(Ocena, null=True, on_delete=models.SET_NULL, related_name='biol_oc',  verbose_name='Biologia ocena')
    inf_oc = models.ForeignKey(Ocena, null=True, on_delete=models.SET_NULL, related_name='inf_oc',  verbose_name='Informatyka ocena')
    sw_wyr = models.BooleanField(default=False, verbose_name='Świadectwo z wyróżnieniem')
    konk_ponad_wyr = models.IntegerField(default=0, verbose_name='Konkurs ponadwojewódzki', choices=KPW)
    konk_woj = models.IntegerField(default=0, verbose_name='Konkurs wojewódzki', choices=KW)
    konk_przedm = models.IntegerField(default=0, verbose_name='Konkurs przedmiotowy', choices=KP)
    konk_inne = models.IntegerField(default=0, verbose_name='Konkursy inne ', choices=KI)
    aktyw_spol = models.IntegerField(default=0, verbose_name='Aktywność społeczna', choices=AS)
    suma_pkt = models.DecimalField(decimal_places=2 , max_digits=5, default=0, editable=False)

    def f_pesel(self,nr):
        if len(nr) == 11:
            for char in list(nr):
                if char.isdigit():
                    status = True
                else:
                    status = False
                    break
        else:
            status = False
        return status

    def __str__(self):
        return f'{self.user.last_name}, {self.user.first_name}'

    def save(self):
        if self.user.is_authenticated and self.user.username=='admin':
            self.suma_pkt = float(self.j_pol_egz) * 0.35 + float(self.mat_egz) *0.35 + float(self.j_obcy_egz) * 0.3 + float(self.j_pol_oc.punkty) + float(self.mat_oc.punkty) + float(self.biol_oc.punkty) + float(self.inf_oc.punkty) + float(self.konk_ponad_wyr) + float(self.konk_woj) + float(self.konk_przedm) + float(self.konk_inne) + float(self.aktyw_spol)
            if self.sw_wyr:
                self.suma_pkt += 7
        # self.user.last_name = (list(self.user.last_name)[0]).upper()+str(''.join(list(self.user.last_name[1:])).lower())
        # self.user.second_name = (list(self.user.second_name)[0]).upper() + str(''.join(list(self.user.second_name[1:])).lower())
        # if self.user.second_name != '':
        #     self.user.second_name = (list(self.user.second_name)[0]).upper() + str(''.join(list(self.user.second_name[1:])).lower())
        super(Kandydat, self).save()



class Upload(models.Model):
    file = models.FileField()