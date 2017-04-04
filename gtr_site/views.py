from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader, RequestContext
from .models import *
import os

# Create your views here.
def index(request):
    return render(request, 'gtr_site/index.html')

def statement_page(request, statement_id):
    state = get_object_or_404(Statement, statement_id=statement_id)
    context  = {'state':state}
    return render(request, 'gtr_site/statement_page.html', context)

def search(request):
    search = request.POST['search']
    from whoosh.index import open_dir
    from whoosh.qparser import MultifieldParser
    ix = open_dir("gtr_site/management/commands/index")
    with ix.searcher() as searcher:
        # https://whoosh.readthedocs.io/en/latest/parsing.html
        mparser = MultifieldParser(["statement_id", "title", "author", "keyword", "context"], ix.schema)
        query = mparser.parse(search)
        results = searcher.search(query)
        print "ffff"
        result_list = [results[i] for i in range(len(results))]
        keywords = [Statement.objects.get(statement_id = result["statement_id"]).get_keywords() for result in result_list]
        contexts = [Statement.objects.get(statement_id = result["statement_id"]).get_contexts() for result in result_list]
        key_con = [Statement.objects.get(statement_id = result["statement_id"]).get_keywords_contexts() for result in result_list]
	print keywords
        unioned_keywords = keywords[0]
        for query_set in keywords:
           unioned_keywords = (unioned_keywords | query_set)
        unioned_keywords.distinct()
        print key_con
        # making a dictionary where the keywords are keys and all contexts that go with those keywords, across the dataset, are in there
        key_con_dict = {}
        for statement in key_con:
           for keyword in statement:
              if keyword.word in key_con_dict:
                 key_con_dict[keyword.word] = key_con_dict[keyword.word] | statement[keyword]
              else:
                 key_con_dict[keyword.word] = statement[keyword]
        for keyword in key_con_dict:
           key_con_dict[keyword] = list(key_con_dict[keyword].distinct())
        print key_con_dict
        context = {'results' : result_list, 'keywords' : keywords, 'contexts' : contexts, 'key_con' : key_con_dict }
    return render(request, 'gtr_site/search_results.html', context)
    
