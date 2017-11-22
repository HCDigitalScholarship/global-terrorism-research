from models import *
from django.db.models import Q
import time
import generate_keywords_from_statement_list

def filter_all():
    pass 
def filter_by_keyword(request):
    search_string = request.GET['search']
    include = []
    exclude = []
    print request.GET
    for key in request.GET:
        key_ON_OFF = request.GET[key]
	if   key_ON_OFF == 'key_ON':
            include.append(key)	    
        elif key_ON_OFF == 'key_OFF':
            exclude.append(key)

    # base query without any filtering (including or excluding)
    # we will build it up with relevant filtering
    query =      (
                  Q(title__icontains=search_string) |
                  Q(statement_id__icontains=search_string) |
                  Q(author__person_name__icontains=search_string) |
                  Q(released_by__org_name__icontains=search_string) |
                  Q(keywords__context__word=search_string) |
                  Q(keywords__main_keyword__word=search_string)
                 )

    print "Seaching:", search_string
    print "Including Statements with Keywords:", include 

    if include:
        include_query = Q(keywords__main_keyword__word=include[0]) 
        for keyword in include[1:]:
	    include_query = include_query | Q(keywords__main_keyword__word=keyword) 
        query = query & include_query 

    print "Excluding Statements with Keywords:", exclude
    if exclude:
        exclude_query = Q(keywords__main_keyword__word=exclude[0]) 
        for keyword in exclude[1:]:
	    exclude_query = exclude_query | Q(keywords__main_keyword__word=keyword) 
        query = query & ~exclude_query

    statement_list = Statement.objects.all()
    statement_list = statement_list.filter(query).distinct() 

    keywords_and_counts = generate_keywords_from_statement_list.generate_top_n_keywords(statement_list, 20)

    keywords = [key_count[0] for key_count in keywords_and_counts]

    context = {'results' : statement_list, 'keywords' : keywords, 'keywords_and_counts' : keywords_and_counts, 'search' : search_string}
    return context 

def filter_by_context():
    pass
def filter_by_keycon():
    pass
