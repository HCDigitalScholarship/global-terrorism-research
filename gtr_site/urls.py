from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search_results/$', views.search, name='search'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^keyword-autocomplete/$', views.Keywords_Autocomplete.as_view(create_field='statement_keywords'), name='keyword-autocomplete'),
    url(r'^context-autocomplete/$', views.Contexts_Autocomplete.as_view(create_field='statement_contexts'), name='context-autocomplete'),
    url(r'^(?P<statement_id>.+)/$', views.statement_page, name='statement'),
    #url(r'^keyword-autocomplete/$', views.Keywords_Autocomplete.as_view(), name='keywords-autocomplete'), 
]
