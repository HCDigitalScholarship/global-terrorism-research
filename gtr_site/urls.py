from django.conf.urls import url

from . import views
from gtr_site.views import *

app_name = 'gtr_site'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^search_results/$', views.CustomSearchView.as_view(), name='search'),
    url(r'author_page/$', views.author_page, name='author_page'),
    url(r'^search_results/$', views.search, name='search'),
    url(r'^about/$', views.about, name='about'),
    url(r'^map/$', views.map, name='map'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^statements/$', views.statements, name='statements'),
    url(r'^advanced_search/$', views.advanced_search_page, name='advanced-search'),
    url(r'^advanced_search_submitted$', views.advanced_search_submit, name='advanced-search-submit'),
    url(r'^resources/$', views.ResourcesList.as_view(), name='resources'),
    url(r'^resources/([\w-]+)/$', views.ResourcesList.as_view(), name='resources'),
    url(r'^resource_results/$', views.resource_search, name='resource-results'),
    url(r'api/v1/keyword/$', GenerateKeywords.as_view(), name='generate-keywords'),
    url(r'^(?P<statement_id>.+)/$', views.statement_page, name='statement'),
]
