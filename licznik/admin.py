from django.contrib import admin

# Register your models here.
from .models import *


#
# class KandydatAdmin(admin.ModelAdmin):
#     readonly_fields = ('user_id',)
# admin.site.register(Kandydat, KandydatAdmin)


admin.site.register(User)
admin.site.register(Klasa)
admin.site.register(Oryginal)
admin.site.register(Upload)
admin.site.register(Kandydat)
admin.site.register(Ocena)