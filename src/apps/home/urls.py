from django.conf.urls import url
from .views import LoginView, logout


urlpatterns = [
    url(r'^$', LoginView.as_view(), name='login'),
    url(r'^logout/$', logout, name='logout'),
]
