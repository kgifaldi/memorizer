from django.conf.urls import url

from . import views

app_name="memorizer"

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^main/$', views.main, name='main'),
    url(r'^learn/$', views.learn, name='learn'),
    url(r'^add/$', views.add, name='add'),
]
