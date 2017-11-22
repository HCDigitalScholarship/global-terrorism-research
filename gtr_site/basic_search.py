from models import *
from django.db.models import Q
import time
import generate_keywords_from_statement_list

"""
The opposite of advanced search, the function takes just the query a user gives it and looks for statements with matching keywords, contexts,
containment in the title.
"""
def basic_search(request):
    search_string = request.GET['search']
    print "excuting basic search"
    
    start = time.time()
    statement_list = Statement.objects.all()
    
    # check title, statement_id, author, and orgnames for containment of search_string
    statement_list = statement_list.filter(
       Q(title__icontains=search_string) | Q(statement_id__icontains=search_string) |
       Q(author__person_name__icontains=search_string) | Q(released_by__org_name__icontains=search_string) |
       Q(keywords__main_keyword__word=search_string) | Q(keywords__context__word=search_string)
    ).distinct() 
    print "generating statement_list took", time.time() - start, "seconds"

    # now generate the list of keywords
    # This is a little slow
    start = time.time()
    keywords_and_counts = generate_keywords_from_statement_list.generate_top_n_keywords(statement_list, 20)
    keywords = [key_count[0] for key_count in keywords_and_counts]
    print "generating keywords took", time.time() - start, "seconds"

    context = {'results' : statement_list, 'keywords' : keywords, 'keywords_and_counts' : keywords_and_counts, 'search' : search_string}
    return context 

