from models import *
from django.db.models import Q
import time
import generate_keywords_from_statement_list
import advanced_search
import datetime
def filter_all():
    pass
def filter_by_keyword(request):
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
    query = advanced_search.advanced_search_make_query(request)
    # query = request.POST.get('search', False)

    print "Query: ",query
    statement_list = Statement.objects.all()
    statement_list = statement_list.filter(query).distinct()

    print "Including Statements with Keywords:", include

    if include:
        include_query = Q(keywords__main_keyword__word=include[0])
        for keyword in include[1:]:
	    include_query = include_query | Q(keywords__main_keyword__word=keyword)
        print "Include query: ", include_query
	statement_list = statement_list.filter(include_query).distinct()

    print "Excluding Statements with Keywords:", exclude
    if exclude:
        exclude_query = Q(keywords__main_keyword__word=exclude[0])
        for keyword in exclude[1:]:
	    exclude_query = exclude_query | Q(keywords__main_keyword__word=keyword)
        query = query & ~exclude_query
        statement_list = statement_list.filter(~exclude_query).distinct()

    include_keywords_and_counts = generate_keywords_from_statement_list.generate_top_n_keywords(statement_list, 20)
    # Add the excluded keywords back to the list, and truncate it to 20 entries.
    exclude_keywords_and_counts = include_keywords_and_counts[:]
    for exc in exclude:
        exclude_keywords_and_counts.insert(0, [exc, 'x'])
    exclude_keywords_and_counts = exclude_keywords_and_counts[:20]

    keywords = [key_count[0] for key_count in include_keywords_and_counts]
    if 'filter_by_date' in request.GET:
        if request.GET['filter_by_date']=='date_ON':
            date_query = filter_by_date(request)
            statement_list =  statement_list.filter(date_query) 

    # now we need to update full_info so it carries over to the next
    # filtering sesh
    
    include_str = '["' + '", "'.join(include) + '"]'
    exclude_str = '["' + '", "'.join(exclude) + '"]'
    context = {'results' : statement_list, 'keywords' : keywords, 'include_buttons': include_str, 'exclude_buttons': exclude_str, 'include_keywords_and_counts': include_keywords_and_counts, 'exclude_keywords_and_counts': exclude_keywords_and_counts, 'full_info' : request.GET['full_info'], 'num_results' : len(statement_list)}
    return context

def filter_by_date(request):
    print request.GET
    for i in range(1, int(request.GET['slider_count']) + 1):
	lowDate = datetime.datetime.strptime(request.GET["date_low"+str(i)][:24], "%a %b %d %Y %X")
	highDate = datetime.datetime.strptime(request.GET["date_high"+str(i)][:24], "%a %b %d %Y %X")
        print lowDate, highDate
	if i==1:
	    date_query = Q(issue_date__gte=lowDate,
                           issue_date__lte=highDate)
	else:
	    date_query = date_query | Q(issue_date__gte=lowDate, issue_date__lte=highDate)
    return date_query
def filter_by_context():
    pass
def filter_by_keycon():
    pass
def update_full_info(include=[], exclude=[]):
    for keyword in include:
        pass
    # here for next time
