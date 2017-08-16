from django.core.management.base import BaseCommand, CommandError
from gtr_site.models import *
from datetime import datetime, date

class Command(BaseCommand):
    help = "Updates everything for searching with whoosh"
    def handle(self, **options):
	import os
	from django.db.models import signals
	from django.conf import settings
	from whoosh import  fields
	# CREATE SCHEMA

	schema = fields.Schema(
				statement_id = fields.ID(stored=True),
				title        = fields.TEXT(stored=True),
				author       = fields.TEXT(stored=True),
				released_by  = fields.TEXT,
				issue_date   = fields.DATETIME(stored=True),
				media_type   = fields.ID(stored=True),
				url          = fields.ID(stored=True, unique=True),
				keyword      = fields.KEYWORD(stored=True, commas=True),
				context      = fields.KEYWORD(stored=True, commas=True)
			     )

	#CREATE INDEX

	import os.path
	from whoosh.index import create_in

	if not os.path.exists("index"):
	    os.mkdir("index")
	ix = create_in("index", schema)


	# WRITE TO INDEX


	from django.conf import settings

	from whoosh.index import open_dir
	ix = open_dir("index")
	writer = ix.writer()
	statements =  Statement.objects.all()
        accu = 0
        print "LEN OF STATEMENTS", len(statements)
	for statement in statements:
          accu+=1
          if accu == 1:
             continue
          print accu
          print statement.show()
          context_list   = []
	  keyword_list = []
          print "LEN OF GET CONTEXTS: ", len(statement.get_contexts())
          print "LEN OF GET KEYWORDS: ", len(statement.get_keywords())
	  for context in statement.get_contexts():
	    context_list.append(context.context_word)
	  for keyword in statement.get_keywords():
	    keyword_list.append(keyword.word)
          print context_list
          print keyword_list
	  print ", ".join(context_list), ", ".join(keyword_list)
	  writer.add_document(
				statement_id = statement.statement_id,
				title        = statement.title,
				author       = statement.author.person_name,
				released_by  = statement.released_by.org_name,
				issue_date   = datetime.combine(statement.issue_date, datetime.min.time()),
				media_type   = statement.media_type,
				url          = statement.full_text,
				keyword      = ", ".join(keyword_list),
				context      = ", ".join(context_list),
			     )
	writer.commit() # note that this should be outside of the for loop
