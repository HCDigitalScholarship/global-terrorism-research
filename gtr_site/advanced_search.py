from models import *
from django.db.models import Q
import time
import generate_keywords_from_statement_list

def advanced_search(request):

    # right now it looks like [Iraq^^Any Field^Iran^OR^Keyword^]
    # so we split on ^ and delete the last one (there is always a tailing empty list
    request_list = request.GET["full_info"].split("^")[:-1]
    print "full info in advanced_search", request.GET["full_info"]
    # request list needs to be split into threes
    # right now it looks like ['Iraq','','Any Field', 'Iran', 'OR', 'Keyword,...]
    # note that the first one will not have the logical operator
    start = time.time() 
    formatted_request_list = []
    ticker = 1
    three_pair = {}
    for item in request_list:
        if ticker == 1:
            three_pair["search_string"] = item
        elif ticker == 2:
            three_pair["logic"] = item
        elif ticker == 3:
            three_pair["field"] = item
            formatted_request_list.append(three_pair)
            three_pair = {}
            ticker = 0 # set to zero since we are going inc after
        ticker += 1

    query = []
    for request_part in formatted_request_list:
            search_string = request_part["search_string"]
            logic         = request_part["logic"]
            field         = request_part["field"]
            query_part = make_query_part(search_string, field)
            if query and query_part:
               if   logic == "AND":
                   query = query & query_part
               elif logic == "OR":
                   query = query | query_part
               elif logic == "NOT":
                   query = query & ~query_part 
            elif query_part:
               query = query_part
            else:
               return False
    statement_list = Statement.objects.all()
    print "Here is your query", query
    statement_list = statement_list.filter(query).distinct()
    print "generating statement_list took", time.time() - start, "seconds"

    # now generate the list of keywords
    # This is a little slow
    start = time.time()
    keywords_and_counts = generate_keywords_from_statement_list.generate_top_n_keywords(statement_list, 20)
    keywords = [key_count[0] for key_count in keywords_and_counts]
    print "generating keywords took", time.time() - start, "seconds"
    for statement in statement_list:
	print statement
    context = {'results' : statement_list, 'keywords' : keywords, 'keywords_and_counts' : keywords_and_counts, 'search' : search_string, 'full_info' : request.GET["full_info"], 'num_results' : len(statement_list)}
    return context


def make_query_part(search_string, field):
    print field
    if field == "Any field":
        query_part = Q( 
                 Q(title__icontains=search_string) |
                 Q(statement_id__icontains=search_string) |
                 Q(author__person_name__icontains=search_string) |
                 Q(released_by__org_name__icontains=search_string) |
                 Q(keywords__main_keyword__word=search_string) |
                 Q(keywords__context__word=search_string)
                ) 
    elif field == 'Title':
        query_part = Q(title__icontains=search_string)
    elif field == 'Statement ID':
        query_part = Q(statement_id__icontains=search_string)
    elif field == 'Author':
        query_part = Q(author__person_name__icontains=search_string)
    elif field == 'Organization':
        query_part = Q(released_by__org_name__icontains=search_string)
    elif field == 'Keyword':
        query_part = Q(keywords__main_keyword__word=search_string)
    elif field == 'Context':
        query_part = Q(keywords__context__word=search_string)
    elif field == 'Keyword in Context':
        # at this point, I assume the user separates it with '->'
        # this may not be what we want 
        try:
            keyword, context = search_string.split('->')
        except ValueError:
            print "Keyword in Context should be in the form 'keyword->Context'"
            return False 
        keyword = keyword.strip()
        context = context.strip()
        query_part = Q(keywords__main_keyword__word=keyword) & Q(keywords__context__word=context)
    else:
        query_part = None
    return query_part

# used for filtering
def advanced_search_make_query(request):
    print request
    request_list = request.GET["full_info"].split("^")
    print "Request List in advanced_search_make_query", request_list
    # request list needs to be split into threes
    # right now it looks like ['Iraq','','Any Field', 'Iran', 'OR', 'Keyword,...]
    # note that the first one will not have the logical operator
    formatted_request_list = []
    ticker = 1
    three_pair = {}
    for item in request_list:
        if ticker == 1:
            three_pair["search_string"] = item
        elif ticker == 2:
            three_pair["logic"] = item
        elif ticker == 3:
            three_pair["field"] = item
            formatted_request_list.append(three_pair)
            three_pair = {}
            ticker = 0 # set to zero since we are going inc after
        ticker += 1

    query = []
    for request_part in formatted_request_list:
            search_string = request_part["search_string"]
            logic         = request_part["logic"]
            field         = request_part["field"]
            query_part = make_query_part(search_string, field)
            if query and query_part:
               if   logic == "AND":
                   query = query & query_part
               elif logic == "OR":
                   query = query | query_part
               elif logic == "NOT":
                   query = query & ~query_part 
            elif query_part:
               query = query_part
    return query
