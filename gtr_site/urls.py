from django.conf.urls import url

from . import views
from gtr_site.views import *

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^search_results/$', views.CustomSearchView.as_view(), name='search'),
    url(r'^search_results/$', views.search, name='search'),
    url(r'^about/$', views.about, name='about'),
    url(r'^map/$', views.map, name='map'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^resources/$', views.resources, name='resources'),
    url(r'^resource_results/$', views.resource_search, name='resource-results'),
    url(r'^keywordincontext_autocomplete/$', views.KeywordInContextAutocomplete.as_view(create_field='word'), name='keywordincontext-autocomplete'),
    url(r'^keywordfilter-autocomplete/$', views.KeywordView.as_view(), name='keywordfilter-autocomplete'),
    url(r'api/v1/keyword/$', GenerateKeywords.as_view(), name='generate-keywords'),
   # url(r'^keyword-autocomplete/$', views.Keywords_Autocomplete.as_view(create_field='statement_keywords'), name='keyword-autocomplete'),
    #url(r'^context-autocomplete/$', views.Contexts_Autocomplete.as_view(create_field='statement_contexts'), name='context-autocomplete'),
    url(r'^(?P<statement_id>.+)/$', views.statement_page, name='statement'),
    #url(r'^keyword-autocomplete/$', views.Keywords_Autocomplete.as_view(), name='keywords-autocomplete'),
]
