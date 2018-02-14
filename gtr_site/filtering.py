from models import *
from django.db.models import Q
import time
import generate_keywords_from_statement_list
import advanced_search
import datetime
import json


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
    start = time.time()
    query = advanced_search.advanced_search_make_query(request) 
    print "Time for generating intial query", time.time() - start
    # query = request.POST.get('search', False)

    print "Query: ", query

    start - time.time()
    statement_list = Statement.objects.all()
    statement_list = statement_list.filter(query).distinct()
    print "Time for all unique_keywords", time.time() - start

    print "Including Statements with Keywords:", include
    start = time.time()
    if include:
        include_query = Q(keywords__main_keyword__word=include[0])
        for keyword in include[1:]:
	    include_query = include_query | Q(keywords__main_keyword__word=keyword)
        print "Include query: ", include_query
	statement_list = statement_list.filter(include_query).distinct()
    print "Time for all including", time.time() - start

    print "Excluding Statements with Keywords:", exclude
    start = time.time()
    if exclude:
        exclude_query = Q(keywords__main_keyword__word=exclude[0])
        for keyword in exclude[1:]:
	    exclude_query = exclude_query | Q(keywords__main_keyword__word=keyword)
        query = query & ~exclude_query
        statement_list = statement_list.filter(~exclude_query).distinct()
    print "Time for all excluding", time.time() - start
    include_keywords_and_counts = generate_keywords_from_statement_list.generate_top_n_keywords(statement_list, 50)
    print include_keywords_and_counts
    # Add the excluded keywords back to the list, and truncate it to 20 entries.
    exclude_keywords_and_counts = include_keywords_and_counts[:]
    for exc in exclude:
        exclude_keywords_and_counts.insert(0, [exc, 'x'])
    exclude_keywords_and_counts = exclude_keywords_and_counts[:20]
    keywords = [key_count[0] for key_count in include_keywords_and_counts]
    if 'filter_by_date' in request.GET:
        if request.GET['filter_by_date']=='date_ON':
            date_query, date_list = filter_by_date(request)
            statement_list =  statement_list.filter(date_query)

    # now we store what we have included and excluded
    # passing it in the context
    # so the checked buttons and the shown statement carry over to the next filtering sesh

    include_str = '["' + '", "'.join(include) + '"]'
    exclude_str = '["' + '", "'.join(exclude) + '"]'
    start = time.time()
    all_keywords = set()
    for statement in statement_list:
        unique_keywords = set(kic.main_keyword.word for kic in statement.keywords.all())
        all_keywords |= unique_keywords
        statement.keyword_str = '|' + '|'.join(unique_keywords) + '|'
    print "Time for all unique_keywords", time.time() - start
    context = {'results' : statement_list,
               'json_results': serialize_statements(statement_list),
               'keywords' : keywords,
               'include_buttons': include_str,
               'exclude_buttons': exclude_str,
               'include_keywords_and_counts': [],
               'exclude_keywords_and_counts': [],
               'full_info' : request.GET['full_info'],
               'num_results' : len(statement_list),
               'all_keywords': json.dumps(list(all_keywords))
              }
    if 'filter_by_date' in request.GET:
        context['slider_count'] = request.GET['slider_count']
        context['date_list'] = date_list
    return context


def filter_by_date(request):
    print request.GET
    date_list = []
    for i in range(1, int(request.GET['slider_count']) + 1):
	lowDate = datetime.datetime.strptime(request.GET["date_low"+str(i)][:24], "%a %b %d %Y %X")
	highDate = datetime.datetime.strptime(request.GET["date_high"+str(i)][:24], "%a %b %d %Y %X")
        date_list.append((lowDate.strftime("%Y, %m, %d"), highDate.strftime("%Y, %m, %d")))
	if i==1:
	    date_query = Q(issue_date__gte=lowDate,
                           issue_date__lte=highDate)
	else:
	    date_query = date_query | Q(issue_date__gte=lowDate, issue_date__lte=highDate)
    return date_query, date_list


def filter_by_context():
    pass


def filter_by_keycon():
    pass


def update_full_info(include=[], exclude=[]):
    for keyword in include:
        pass
    # here for next time


def serialize_statements(statement_list):
    """Serialize a list of Statement objects into a JSON list so that it can be loaded and
    manipulated by the client-side JavaScript.
    """
    return json.dumps([statement_to_dictionary(st) for st in statement_list])

def statement_to_dictionary(statement):
    """Convert a Statement object into a dictionary (in prep for JSON serialization)."""
    keywords = [kic.main_keyword.word for kic in statement.keywords.all()]
    author = statement.author.person_name
    return {'title': statement.title, 'author': author, 'keywords': keywords}
