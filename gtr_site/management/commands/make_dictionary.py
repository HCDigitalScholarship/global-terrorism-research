import csv
import pprint
def main():
   """
	Creates a python dictionary with statement id's as keys to other dictionaries that then have all the relevant information from our spread sheets e.g.:
	
	{"STATEMENT_ID" : {"keyword": [keyword1, keyword2], "context": [(keyword1, context1),(keyword1,context2)]}}
   """

   #with open('/srv/global-terrorism-research/statements_loading_data.csv') as f:
   with open('statements_loading_data.csv') as f:
      statement_dictionary = {}
      for row in csv.DictReader(f, skipinitialspace=True):
	 statement_id = row["statement_id"]
	 context      = row["context"]
	 keyword      = row["keyword"] 
         if statement_id not in statement_dictionary:
            # add a new key!
            if context == ' ' or context == '':
               row["keyword"] = set([keyword])
	       row["context"] = []
            else:
               row["keyword"] = set([keyword])
	       # you need to swap them, because drupal does some strange things
	       # you can look at the sheet, it is just this way
               row["context"] = [(context,keyword)]
            #entry_dictionary["keyword"] = [entry_dictionary["keyword"]]
            statement_dictionary[statement_id] = row
         else:
	    # key already exists
	    # we either add a new keyword to this statment or
	    # add a keyword and a keyword context pair
	    statement = statement_dictionary[statement_id]
	    if context == ' ' or context == '':
               statement["keyword"].add(keyword)
            else:
               statement["keyword"].add(keyword)
	       # you need to swap them, because drupal does some strange things
	       # you can look at the sheet, it is just this way
               statement["context"].append((context,keyword))

            # just add key word and/or context
            #statement_dictionary[row['statement_id']]["keyword"].append(row['keyword'])
            #context = row["context"]
            #if context != ' ':
            #   statement_dictionary[row['statement_id']]['context'].append((row['keyword'],context))
      #print "\nSTATEMENT DICTIONARY START\n"
      #pprint.pprint(statement_dictionary)
      #print "\nSTATEMENT DICTIONARY END\n"
      #pprint.pprint(statement_dictionary)
      return statement_dictionary

main()
