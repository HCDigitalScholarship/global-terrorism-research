"""
import os, django, sys
from django.conf import settings
sys.path.append('/srv/global-terrorism-research')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gtr.settings")
django.setup()
"""
from models import *
from django.db.models import Q
import time
"""
The opposite of advanced search, the function takes just the query a user gives it and looks for statements with matching keywords, contexts,
containment in the title.
"""
def basic_search(request):
    search_string = request.GET['search']
    print "excuting basic search"
    # First, let's check if it is a keyword
    try:
        tt = Keyword.objects.get(word=search_string)
    except Keyword.DoesNotExist:
	print "Welp,", search_string, "is not a keyword"
	print 
        tt = None
    start = time.time()
    qs_list = Statement.objects.all()
    # check title, statement_id, author, and orgnames for containment of search_string
    qs_list = qs_list.filter(
       Q(title__icontains=search_string) | Q(statement_id__icontains=search_string) |
       Q(author__person_name__icontains=search_string) | Q(released_by__org_name__icontains=search_string) |
       Q(keywords__main_keyword__word=search_string) | Q(keywords__context__word=search_string)
    ).distinct() 
    print "generating qs_list took", time.time() - start, "seconds"
    
    """ 
    # I think qs_list is lazy, but I want to use the items
    # there is probably a better way of doing this with 'yield', but I don't know much about that
    statement_list = []
    for lazy_statement in qs_list:
        print lazy_statement
	statement_list.append(Statement.objects.get(statement_id = lazy_statement["statement_id"]))
    """
   
    # now generate the list of keywords
    # This is a little slow
    start = time.time()
    keywords = set()
    keyword_sets = [set(statement.get_keywords()) for statement in qs_list]
    keywords = keywords.union(*keyword_sets)
    print "generating keywords took", time.time() - start, "seconds"
    context = {'results' : qs_list, 'keywords' : keywords, 'search' : search_string}
    return context 

# It is tricky to get this test working because you need to configure Django settings
# You can see me try to do this at the top (now commented out)
# Basically, I couldn't get this to be useful, but I'm leaving it incase someone else wants to test
# with this method and can figure it out?

# fake request for testing
class fake_request:
    def __init__(self, search_string):
	self.GET = {'search' : search_string}

def main_test():
    myrequest = fake_request("Iraq")
    basic_search(myrequest)

if __name__ == "__main__":
    main_test()
