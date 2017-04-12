from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader, RequestContext
from .models import *
import os

# Create your views here.
def index(request):
    return render(request, 'gtr_site/index.html')

def about(request):
    return render(request, 'gtr_site/about.html')

def contact(request):
    return render(request, 'gtr_site/contact.html')

def statement_page(request, statement_id):
    state = get_object_or_404(Statement, statement_id=statement_id)
    context  = {'state':state}
    return render(request, 'gtr_site/statement_page.html', context)

def search(request):
    if 'search' in request.POST:
	    search = request.POST['search']
	    from whoosh.index import open_dir
	    from whoosh.qparser import MultifieldParser
	    from whoosh.query import *
	    ix = open_dir("index")
	    with ix.searcher() as searcher:
		# https://whoosh.readthedocs.io/en/latest/parsing.html
		mparser = MultifieldParser(["statement_id", "title", "author", "keyword", "context"], ix.schema)
	 	filter_request = False
                if 'Filter' in request.POST:
                   # because to the best of my knowledge I can't make an empty query
		   # I need to do this little hack
	 	   filter_request = True
		   no_con_yet     = True
		   no_key_yet     = True
		   no_key_con_yet = True

                   for key in request.POST:
		      print request.POST[key]
		      print "need to turn on", key
		      if request.POST[key]=='con_ON':
			if no_con_yet:
			  con_query = Term("context", key)
			  no_con_yet = False
			else:
			  con_query = con_query | Term("context", key)
		      elif request.POST[key]=='key_ON':
			if no_key_yet:
			  key_query = Term("keyword", key)
			  no_key_yet = False
			else:
			  key_query = key_query | Term("keyword", key)
		      elif request.POST[key]=='key_con_ON':
			# I am breaking these on underscores,
			# so there will be problems if a key/con has underscores
			keyword, context = key.split("_")

			key_con = Term("keyword", keyword)
			key_con = key_con & Term("context", context)

			if no_key_con_yet:
			  key_con_query = key_con
			  no_key_con_yet = False
			else:
			  key_con_query = key_con_query | key_con
			
		      # So they are just not included in the query if they are off; this is a reminder that we might want exclude functionality
		query = mparser.parse(search)
		#allow = query.Term("context", "Chastisement")
		if filter_request and not no_con_yet:
		  query = query & con_query 
	          print con_query
		if filter_request and not no_key_yet:
		  query = query & key_query
		  print key_query
		if filter_request and not no_key_con_yet:
		  query = query & key_con_query
		print query
		results = searcher.search(query)

                # if we returned no results, we need to just return here
		if len(results) == 0:
		  return render(request,  'gtr_site/search_results.html')


		result_list = [results[i] for i in range(len(results))] # convert from query type to normal list
		keywords = [Statement.objects.get(statement_id = result["statement_id"]).get_keywords() for result in result_list]
		contexts = [Statement.objects.get(statement_id = result["statement_id"]).get_contexts() for result in result_list]
		key_con  = [Statement.objects.get(statement_id = result["statement_id"]).get_keywords_contexts() for result in result_list]
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
		context = {'results' : result_list, 'keywords' : keywords, 'contexts' : contexts, 'key_con' : key_con_dict, 'search' : search }
	    return render(request, 'gtr_site/search_results.html', context)
    else:
       print request.POST
       return render(request, 'gtr_site/search_results.html')
