from django.conf.urls import url

from . import views
from gtr_site.views import *
from django.contrib.flatpages import views as flat_views

app_name = 'gtr_site'

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    # It looks like flatpages don't work for the index view, so ignore next line :(
    url(r'^$', flat_views.flatpage, {'url': '/'}, name='index'),    
    #url(r'^search_results/$', views.CustomSearchView.as_view(), name='search'),
    url(r'author/(?P<author_name>.+)/$', views.author_page, name='author_page'),
    url(r'^search_results/$', views.search, name='search'),
    url(r'^about/$', flat_views.flatpage, {'url': '/about/'}, name='about'),
    #url(r'^about/$', views.about, name='about'),
    url(r'^lists/$', views.lists, name='lists'),
    url(r'^list/(?P<list>.+)/$', views.list, name='list'),
    url(r'^map/$', views.map, name='map'),
    url(r'^contact/$', flat_views.flatpage, {'url': '/contact/'}, name='contact'),
    url(r'^search-help/$', flat_views.flatpage, {'url': '/search-help/'}, name='search-help'),
    url(r'^statements/$', views.statements, name='statements'),
    url(r'^keyword/(?P<keyword_word>.+)/$', views.keyword_browse, name='keyword-browse'),
    url(r'^keywordcontext/(?P<keyword_word>.+)/(?P<context_word>.+)/$', views.keyword_context_browse, name='keyword-context-browse'),
    url(r'^advanced_search/$', views.advanced_search_page, name='advanced-search'),
    url(r'^advanced_search_submitted$', views.advanced_search_submit, name='advanced-search-submit'),
    url(r'^resources/$', views.ResourcesList.as_view(), name='resources'),
    url(r'^resources/([\w-]+)/$', views.ResourcesList.as_view(), name='resources'),
    url(r'^resource_results/$', views.resource_search, name='resource-results'),
    url(r'api/v1/keyword/$', GenerateKeywords.as_view(), name='generate-keywords'),
    url(r'^statement/(?P<statement_id>.+)/$', views.statement_page, name='statement'),
]
