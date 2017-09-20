from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader, RequestContext
#from django.models import model.formset_factory
from .models import *
from whoosh.query import *
from datetime import *
from dal import autocomplete
from haystack.generic_views import SearchView
from django.db.models import Q
try:
    from django.urls import reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse_lazy
from django.views import generic, View
from django.http import JsonResponse
from gtr_site.forms import *


import os

#class CustomSearchView(SearchView):
    #pass

# Create your views here.
def index(request):
    print "HOME" 
    return render(request, 'gtr_site/index.html')

def about(request):
    return render(request, 'gtr_site/about.html')

class GenerateKeywords(View):
    def get(self, request, *args, **kwargs):
        #qs = list(Keyword.objects.all())
        #data = {"results": qs}
        #return JsonResponse(data)
      i = 1
      pythondictionary = []
      for each in Keyword.objects.all():
         pythondictionary.append({'id' : i, 'name' : each.word})
         i+=1
      jsondict = json.dumps(pythondictionary)
      print jsondict
      return jsondict


def contact(request):
    return render(request, 'gtr_site/contact.html')

def map(request):
    return render(request, 'gtr_site/map.html')

def statement_page(request, statement_id):
    state = get_object_or_404(Statement, statement_id=statement_id)
    keycondict = state.get_keywords_contexts()
    context  = {'state':state, 'keycondict':keycondict,}
    print "PRINTING KEYWORDS CONTEXTS FOR %s" % state
    print state.get_keywords_contexts()
    return render(request, 'gtr_site/statement_page.html', context)

def resources(request):
    return render(request, 'gtr_site/resources.html')

def resource_search(request):
    print "HELLO WORLD"
    query = request.GET.get("search")
    if query:
       qs_list = Resource.objects.all()
       #complex lookups for various fields
       qs_list = qs_list.filter(
          Q(title__icontains=query) | Q(description__icontains=query) |
          Q(author__icontains=query) | Q(country__icontains=query)
       ).distinct() #these are all the items that can be searched by basic char analysis at the moment.

       #Search results are put into the context dictionary
       context = {
          "results": qs_list
       }
       print "CONTEXT"
       print context

    return render(request, 'gtr_site/resource_results.html', context)

'''class Keywords_Autocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Keyword.objects.none()

        qs = Keyword.objects.all()

        if self.q:
            qs = qs.filter(word__istartswith=self.q)
        return qs'''


class KeywordInContextAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
       if not self.request.user.is_authenticated():
          return KeywordInContext.objects.none()
       qs = Keyword.objects.all()
       if self.q:
          qs = qs.filter(word__istartswith=self.q)
       return qs

class KeywordAutocomplete(autocomplete.Select2QuerySetView):
   def get_queryset(self):
      if not self.request.user.is_authenticated():
          print "user not authenticated so autocomplete doesn't work."
          return Keyword.objects.none()
      qs = Keyword.objects.all()
      if self.q:
         qs = qs.filter(worrd__istartswith=self.q)
      return qs 


class KeywordView(generic.UpdateView):
    model = Keyword
    form_class = KeywordFilterForm 
    template_name = 'search/search.html'
    success_url = reverse_lazy('search')

    def get_object(self):
        return Keyword.objects.first()

"""class Contexts_Autocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
      if not self.request.user.is_authenticated():
         return Context.objects.all()
      qs = Context.objects.all()
      if self.q:
         qs = qs.filter(context_word__istartswith=self.q)
      return qs"""

def search(request):
    qs_list = Statement.objects.all()
    print "HELLO WORLD"
    query = request.GET.get("search")
    if query:
       if "->" in query:
          print "Keyword context operator detected" 
       qs_list = Statement.objects.all()
       #complex lookups for various fields
       qs_list = qs_list.filter(
          Q(title__icontains=query) | Q(statement_id__icontains=query) |
          Q(author__person_name__icontains=query) | Q(released_by__org_name__icontains=query)
       ).distinct() #these are all the items that can be searched by basic char analysis at the moment.
       
       set_of_keywords = Keyword.objects.all()
       #Search results are put into the context dictionary
       context = {
          "results": qs_list, "keywords": set_of_keywords,
       }
       print "QS_LIST: "
       print qs_list
       #print "CONTEXT: "
       #print context
       #for x in qs_list:
           #print "URL: "
           #print x.get_absolute_url()
    #if 'search' in request.POST:
        #print "HELLO WORLD FROM CONDITIONAL!"
        #search = request.POST['search']
        #print "SEARCH: ", search
       return render(request, 'search/search.html', context)


"""

def search(request):
    print "Old search"
    print request.GET
    if 'search' in request.GET:
            print "HELLO WORLD FROM CONDITIONAL!" 
	    search = request.GET['search']
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
                if 'Filter' in request.GET:
		   if "filter_by_date" in request.GET:
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

                   for key in request.GET:
		      print request.GET[key]
		      print "working with", key
		      if request.GET[key]=='con_ON':
			if no_con_yet:
			  con_query = Term("context", key)
			  no_con_yet = False
			else:
			  con_query = con_query | Term("context", key)
		      elif request.GET[key]=='key_ON':
			if no_key_yet:
			  key_query = Term("keyword", key)
			  no_key_yet = False
			else:
			  key_query = key_query | Term("keyword", key)
		      elif request.GET[key]=='key_con_ON':
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
			lowDate = datetime.strptime(request.GET[key][:24], "%a %b %d %Y %X")
		      elif filter_date and key == "date_high":
			highDate = datetime.strptime(request.GET[key][:24], "%a %b %d %Y %X")
		      elif request.GET[key]=='con_OFF':
		        # now we do the excluding, which is very similar
			if ex_no_con_yet:
			  ex_con_query = Term("context", key)
			  ex_no_con_yet = False
			else:
			  ex_con_query = ex_con_query | Term("context", key)
		      elif request.GET[key]=='key_OFF':
			if ex_no_key_yet:
			  ex_key_query = Term("keyword", key)
			  ex_no_key_yet = False
			else:
			  ex_key_query = ex_key_query | Term("keyword", key)
		      elif request.GET[key]=='key_con_OFF':
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
		  for i in range(1, int(request.GET['slider_count']) + 1):
			lowDate = datetime.strptime(request.GET["date_low"+str(i)][:24], "%a %b %d %Y %X")
			highDate = datetime.strptime(request.GET["date_high"+str(i)][:24], "%a %b %d %Y %X")
		  	if i==1:
			  date_query = DateRange("issue_date", lowDate, highDate)
			else:
			  date_query = date_query | DateRange("issue_date", lowDate, highDate)
		  query = query & date_query
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
		  return render(request,  'search/search.html')

                print results, "RESULTS"
                print len(results)
                result_list = []
                for r in results:
                   print r
                   result_list.append(r)
                print "all done"
		#result_list = [results[i] for i in range(len(results))] # convert from query type to normal list
                print "Success!"
		keywords = [Statement.objects.get(statement_id = result["statement_id"]).get_keywords() for result in result_list] #get all statements.keyword_in_contexts
		#contexts = [Statement.objects.get(statement_id = result["statement_id"]).get_contexts() for result in result_list]
                #Does the above line need to be here anymore if we have removed the idea of contexts as an entity unique from keywords?
		key_con  = [Statement.objects.get(statement_id = result["statement_id"]).get_keywords_contexts() for result in result_list] #So does this conflict with 
                #the line that performs gett_keywords? we're getting all keywordincontexts twice.
                print "KEYWORDS (only the main_keyword objects of the KeywordInContext's associated with this statement)"
		print keywords
                print "list of tuple of keyword context pairs"
                print key_con
                
		#unioned_keywords = keywords[0]
		#for query_set in keywords:
		   #unioned_keywords = (unioned_keywords | query_set)
		#unioned_keywords.distinct()
		#print key_con
                
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
                #The below line should be deprecated because contexts and key_con_dict are no longer necessary. At all.
		context = {'results' : result_list, 'keywords' : keywords, 'contexts' : contexts, 'key_con' : key_con_dict, 'search' : search }
	    return render(request, 'search/search.html', context)
    else:
       print request.GET
       return render(request, 'search/search.html')
"""
