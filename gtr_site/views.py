from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader, RequestContext
from .models import *
from whoosh.query import *
from datetime import *
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
	    from whoosh.qparser import MultifieldParser, QueryParser
	    from whoosh.qparser.dateparse import DateParserPlugin 
	    ix = open_dir("index")
	    with ix.searcher() as searcher:
		# https://whoosh.readthedocs.io/en/latest/parsing.html
		mparser = MultifieldParser(["statement_id", "title", "author", "keyword", "context"], ix.schema)
		mparser.add_plugin(DateParserPlugin())
		dateparse = QueryParser("issue_date", schema= ix.schema)
		dateparse.add_plugin(DateParserPlugin()) # http://whoosh.readthedocs.io/en/latest/dates.html
	 	filter_request = False
                if 'Filter' in request.POST:
		   if "filter_by_date" in request.POST:
			filter_date = True
		   else:
			filter_date = False
                   # because to the best of my knowledge I can't make an empty query
		   # I need to do this little hack
	 	   filter_request = True
		   no_con_yet     = True
		   no_key_yet     = True
		   no_key_con_yet = True
		   
		   ex_no_con_yet     = True
		   ex_no_key_yet     = True
		   ex_no_key_con_yet = True


                   for key in request.POST:
		      print request.POST[key]
		      print "working with", key
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
		      elif filter_date and  key == "date_low":
			
			# we need to convert to python date time, then convert it back to a string
			# this seems stupid, and it kind of is
			# but I think it is neccessary to get the tools we are using to
			# work together
			
			# there is also some junk I don't want at the end, string looks like:
			# Mon Jan 01 1990 00:00:00 GMT-0500 (EST)
			# We split on the line:
			# Mon Jan 01 1990 00:00:00| GMT-0500 (EST)
 			
			#lowDate = request.POST[key][:24]
			lowDate = datetime.strptime(request.POST[key][:24], "%a %b %d %Y %X")
		      elif filter_date and key == "date_high":
			highDate = datetime.strptime(request.POST[key][:24], "%a %b %d %Y %X")
		      elif request.POST[key]=='con_OFF':
		        # now we do the excluding, which is very similar
			if ex_no_con_yet:
			  ex_con_query = Term("context", key)
			  ex_no_con_yet = False
			else:
			  ex_con_query = ex_con_query | Term("context", key)
		      elif request.POST[key]=='key_OFF':
			if ex_no_key_yet:
			  ex_key_query = Term("keyword", key)
			  ex_no_key_yet = False
			else:
			  ex_key_query = ex_key_query | Term("keyword", key)
		      elif request.POST[key]=='key_con_OFF':
			# I am breaking these on underscores,
			# so there will be problems if a key/con has underscores
			keyword, context = key.split("_")

			ex_key_con = Term("keyword", keyword)
			ex_key_con = key_con & Term("context", context)

			if ex_no_key_con_yet:
			  ex_key_con_query = ex_key_con
			  ex_no_key_con_yet = False
			else:
			  ex_key_con_query = ex_key_con_query | ex_key_con

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
		
		if filter_request and filter_date:
		  query = query & DateRange("issue_date", lowDate, highDate)
		
		if filter_request and not ex_no_con_yet:
		  query = query - ex_con_query 
		if filter_request and not ex_no_key_yet:
		  query = query - ex_key_query
		if filter_request and not ex_no_key_con_yet:
		  query = query - ex_key_con_query
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
		#if filter_request: # might not actually need this
		context = {'results' : result_list, 'keywords' : keywords, 'contexts' : contexts, 'key_con' : key_con_dict, 'search' : search }
	    return render(request, 'gtr_site/search_results.html', context)
    else:
       print request.POST
       return render(request, 'gtr_site/search_results.html')
