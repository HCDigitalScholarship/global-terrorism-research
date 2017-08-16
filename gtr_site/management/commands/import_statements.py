import sys
import os
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from gtr_site.models import *
import make_dictionary


class Command(BaseCommand):
   help = "Imports/updates the database"
   def add_arguments(self,parser):
      parser.add_argument("inputCSVFile",nargs=1, type=str, help="Name of file to import (include .csv)")

   def handle(self, *args, **options):
      MEDIA_TYPE_DICTIONARY = {'Audio Transcript' : 'AU', 'Text' : 'TX', 'Video Transcript' : 'VD', 'Tweet' : 'TW'}
      statement_dictionary = make_dictionary.main()
      #accu=0
      #print "STATEMENT DICTIONARY\n", statement_dictionary
      accu1 = 0
      print "BEGINNING STATEMENT IMPORTATION" 
      for statement_key in statement_dictionary:
         #iterating over each statement. To monitor progress, it would be best to put a print statement here.
         accu1 +=1
         print "STATEMENT_KEY IN STATEMENT DICTIONARY FOR ITER ", accu1
         print statement_key
         statement = statement_dictionary[statement_key]
         Organization.objects.update_or_create(org_name = "al-Qaeda")
         Person.objects.update_or_create(person_name = statement["author"])
         '''if (statement["issue_date"] == ''):
            print "detected empty issue_date"
            statement["issue_date"] = Non'''
         try:
             Statement.objects.update_or_create(
              statement_id = statement["statement_id"],
              defaults = {
                'title'       : statement["title"],
                'issue_date'  : datetime.strptime(statement["issue_date"],"%m/%d/%Y"),
                'author'      : Person.objects.get(person_name = statement["author"]),
                'released_by' : Organization.objects.get(org_name = "al-Qaeda"),
                'media_type'  : MEDIA_TYPE_DICTIONARY[statement['media_type']] ,
                'full_text'   : statement['link'],
               }
             )
         except:
             Statement.objects.update_or_create(
               statement_id = statement["statement_id"],
               defaults = {
                 'title'       : statement["title"],
                 'issue_date'  : None,
                 'author'      : Person.objects.get(person_name = statement["author"]),
                 'released_by' : Organization.objects.get(org_name = "al-Qaeda"),
                 'media_type'  : MEDIA_TYPE_DICTIONARY[statement['media_type']] ,
                 'full_text'   : statement['link'],
               }
             )
 
         cur_statement = Statement.objects.get(statement_id = statement["statement_id"])
         Statement.objects.get(statement_id = statement["statement_id"]).save()
         #accu +=1
         #print "ITERATION, ", accu
         #print "CUR_STATEMENT'S VALUE: \n", cur_statement
         for keyword, contextlist in statement['context']:
             print "KEYWORD: ", keyword
             this_keyword, _ = Keyword.objects.get_or_create(word=keyword,)
             #this_keyword.statement.add(cur_statement)
             #print "THIS_KEYWORD: ", this_keyword
             #obj, _ = KeywordInContext.objects.get_or_create(keyword=this_keyword)
             if len(contextlist) == 0:
                 #debug: We can't just set a "None" type to a context's null field.
                 print "SOLO KEYWORD/KEYWORDINCONTEXT WITH BLANK CONTEXT: ", this_keyword 
                 obj, _ = KeywordInContext.objects.update_or_create(main_keyword = this_keyword, context=None)
                 cur_statement.keywords.add(obj)
             for each in contextlist:
                 print "CONTEXT IN STATEMENT ID ", cur_statement.id, " : ", each
                 #obj.contexts.add(Keyword.objects.get(word=context))
                 try:
                   print "getting context"
                   a = Keyword.objects.get(word=each)
                   print a
                 except:
                   "ERROR IN GETTING CONTEXT"
                   #"MAKING NEW KEYWORD FOR CONTEXT"
                   new_kword = Keyword.create_keyword(word=each)
                   new_kword.save()
                 obj, _ = KeywordInContext.objects.update_or_create(main_keyword = this_keyword, context=Keyword.objects.get(word=each))
                 cur_statement.keywords.add(obj)   
             #cur_statement.keywords.add(obj)
      print "FINISHED"

         
'''         for keyword in statement["keyword"]:
            Keyword.objects.update_or_create(
              word = keyword
            )
            Keyword.objects.get(word = keyword).statement.add(cur_statement)
            #Populating statements with keywords.
            #Statement.objects.get(statement contains keyword, id=cur_statement.id).statement-keywords_set.add(Keyword.objects.get(word = keyword))
         for context in statement["context"]:
            Context.objects.update_or_create(
              context_word = context[1]
            )
            Context.objects.get(context_word = context[1]).keyword.add(Keyword.objects.get(word = context[0]))
            Context.objects.get(context_word = context[1]).statement.add(cur_statement)
            #Populating statements with contexts
            #Statement.objects.get(statement contains context word, id=cur_statement).statement-contexts_set.add(Context.objects.get(context_word = context[1]))
            #may need to remove _set.
         '''
            
