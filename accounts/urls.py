from django.urls import path
#
from . import views
from .views import SignUpView, success


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('success/', views.success, name="success"),
    # path('accounts/password_reset/', name='password_reset'),
    # path('accounts/password_reset/done/', name='password_reset_done'),
]