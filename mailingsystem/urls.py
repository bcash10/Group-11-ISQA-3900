from django.urls import include, path
from .views import index


urlpatterns = [
    path('', index, name='index')
]
from django.urls import include, path
from .views import index


urlpatterns = [
    path('', index, name='index'),
    path('getdata/', index, name='views.index'),
]
