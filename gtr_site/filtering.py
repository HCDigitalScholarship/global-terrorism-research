from models import *
from django.db.models import Q
import time

def filter_all():
    pass 
def filter_by_keyword(request):
    search_string = request.GET['search']
    include = []
    exclude = []
    for key in request.GET:
        key_ON_OFF = request.GET[key]
	if   key_ON_OFF == 'key_ON':
            include.append(key)	    
        elif key_ON_OFF == 'key_OFF':
            exclude.append(key)

    print "Seaching:", search_string
    print "Including Statements with Keywords:", include
    if include:
        include_query = Q(keywords__main_keyword__word=include[0]) 
        for keyword in include[1:]:
	    include_query = include_query | Q(keywords__main_keyword__word=keyword) 
        print include_query
    print "Excluding Statements with Keywords:", exclude
    if exclude:
        exclude_query = Q(keywords__main_keyword__word=exclude[0]) 
        for keyword in exclude[1:]:
	    exclude_query = exclude_query | Q(keywords__main_keyword__word=keyword) 
        print exclude_query

    qs_list = Statement.objects.all()
    qs_list = qs_list.filter(
       (Q(title__icontains=search_string) | Q(statement_id__icontains=search_string) |
       Q(author__person_name__icontains=search_string) | Q(released_by__org_name__icontains=search_string) |
       Q(keywords__context__word=search_string) | Q(keywords__main_keyword__word=search_string)) & include_query & ~exclude_query  
    ).distinct() 

    # I used this twice (also in single_search.py basic_search)
    # maybe it should be it's own function 
    start = time.time()
    keywords = set()
    keyword_sets = [set(statement.get_keywords()) for statement in qs_list]
    keywords = keywords.union(*keyword_sets)
    print "generating keywords took", time.time() - start, "seconds"
    context = {'results' : qs_list, 'keywords' : keywords, 'search' : search_string}
    return context 

    retunr 
def filter_by_context():
    pass
def filter_by_keycon():
    pass
