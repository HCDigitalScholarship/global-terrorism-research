import sys
import os
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from gtr_site.models import *
import make_dictionary

class Command(BaseCommand):
   help = "Imports/updates the database"

   """
   # we no longer use this parameter, but I am leaving it in here in case someone wants to add a
   def add_arguments(self,parser):
      parser.add_argument("inputCSVFile",nargs=1, type=str, help="Name of file to import (include .csv)")
   """
   def handle(self, *args, **options):
      MEDIA_TYPE_DICTIONARY = {'Audio Transcript' : 'AU', 'Text' : 'TX', 'Video Transcript' : 'VD', "Tweet" : "TW"}
      statement_dictionary = make_dictionary.main()
      Organization.objects.update_or_create(org_name = "al-Qaeda")
      for statement_key in statement_dictionary:
         statement = statement_dictionary[statement_key]
         Person.objects.update_or_create(person_name = statement["author"])
         if statement["issue_date"] != '':
	    date = datetime.strptime(statement["issue_date"],"%m/%d/%Y")
	 else:
	    date = None
         Statement.objects.update_or_create(
           statement_id = statement["statement_id"],
           defaults = {
             'title'       : statement["title"],
             'issue_date'  : date, 
             'author'      : Person.objects.get(person_name = statement["author"]),
             'released_by' : Organization.objects.get(org_name = "al-Qaeda"),
             'media_type'  : MEDIA_TYPE_DICTIONARY[statement['media_type']] ,
             'full_text'   : statement['link'],
           }
         )
         cur_statement = Statement.objects.get(statement_id = statement["statement_id"])
         for keyword in statement["keyword"]:
            Keyword.objects.update_or_create(
              word = keyword
            )

            #Keyword.objects.get(word = keyword).statement.add(cur_statement)
            #Populating statements with keywords.

            #Statement.objects.get(statement contains keyword, id=cur_statement.id).statement-keywords_set.add(Keyword.objects.get(word = keyword))
         for context in statement["context"]:
	    # if the context that is about to be used doesn't exsist
	    # add it (keywords and contexts are the same at this point)
	    
            keyword = context[0]
	    keyword_obj, created_keyword = Keyword.objects.get_or_create(
	       word = keyword
	    )
	    print created_keyword
	    context = context[1]
	    context_obj, created_context = Keyword.objects.get_or_create(
	      word = context
	    )
	    # now add the keyword context pairing
	    KIC, created_KIC = KeywordInContext.objects.get_or_create(
	      main_keyword = keyword_obj,
	      context      = context_obj
	    )

	    cur_statement.keywords.add(KIC.id) 
            #Context.objects.get(context_word = context[1]).keyword.add(Keyword.objects.get(word = context[0]))
            #Context.objects.get(context_word = context[1]).statement.add(cur_statement)
            #Populating statements with contexts
            #Statement.objects.get(statement contains context word, id=cur_statement).statement-contexts_set.add(Context.objects.get(context_word = context[1]))
            #may need to remove _set.
