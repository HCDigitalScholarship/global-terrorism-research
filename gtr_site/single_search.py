import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gtr.settings")

from gtr_site.models import *


def single_search(request):
    search_string = request.GET['search']
    # First, if it is a keyword
    Keyword.objects.get(word=search_string)


# fake request for testing
class fake_request:
    def __init__(self, search_string):
	self.GET = {'search' : search_string}

def main_test():
    myrequest = fake_request("Iraq")
    single_search(myrequest)

main_test()
