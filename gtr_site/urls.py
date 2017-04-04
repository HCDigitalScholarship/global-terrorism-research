from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search_results/$', views.search, name='search'),
    url(r'^(?P<statement_id>.+)/$', views.statement_page, name='statement'),
]
