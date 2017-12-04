from models import *
from django.db.models import Q
import time
import generate_keywords_from_statement_list

def advanced_search(request):
    print request.GET
    
