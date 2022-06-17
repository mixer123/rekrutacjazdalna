from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views



urlpatterns = [


    path('', views.starting_page, name="starting-page"),
    path('zapisz/', views.zapisz, name="zapisz-page"),
    path('wybierzklase/', views.chooseclas, name="chooseclas-page"),
    path('zmienlogin/', views.zmienlogin, name="zmienlogin-page"),
    path('zmienklase/', views.zmienclas, name="zmienclas-page"),
    path('zestawienieklasy/', views.zestawienieklasy, name="zestawienieklasy-page"),
    path('zestawienie/', views.zestawienie, name="zestawienie-page"),
    # path('zestawienie/',views.zestawienie, name="zestawienie-page" ),
    # path('admin/', views.admin_page, name="admin-page"),
    # path('uploadfile/', views.uploadfile, name="uploadfile-page"),
    # path('error/', views.error, name="error-page"),
]


admin.site.site_header = 'Rekrutacja 2022'                    # default: "Django Administration"
admin.site.index_title = 'Rekrutacja 2022'                 # default: "Site administration"
admin.site.site_title = 'Rekrutacja 2022' # default: "Django site admin"
