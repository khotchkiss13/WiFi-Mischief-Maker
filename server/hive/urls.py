from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^crack/$', views.crack, name='crack'),
]