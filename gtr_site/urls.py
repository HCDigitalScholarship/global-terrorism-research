from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search_results/$', views.CustomSearchView.as_view(), name='search'),
    url(r'^about/$', views.about, name='about'),
    url(r'^map/$', views.map, name='map'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^keywordincontext-autocomplete/$', views.KeywordInContextAutocomplete.as_view(create_field='word'), name='keywordincontext-autocomplete',),
   # url(r'^keyword-autocomplete/$', views.Keywords_Autocomplete.as_view(create_field='statement_keywords'), name='keyword-autocomplete'),
    #url(r'^context-autocomplete/$', views.Contexts_Autocomplete.as_view(create_field='statement_contexts'), name='context-autocomplete'),
    url(r'^(?P<statement_id>.+)/$', views.statement_page, name='statement'),
    #url(r'^keyword-autocomplete/$', views.Keywords_Autocomplete.as_view(), name='keywords-autocomplete'),
]
