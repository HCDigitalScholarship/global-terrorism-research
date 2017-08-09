import csv
import pprint
def main():
   print "hello World!"
   #with open('/srv/global-terrorism-research/statements_loading_data.csv') as f:
   with open('statements_loading_data.csv') as f:
      statement_dictionary = {}
      for row in csv.DictReader(f, skipinitialspace=True):
         if row["statement_id"] not in statement_dictionary:
            # add a new key!
            entry_dictionary = {k:v for k,v in row.items()}
            if entry_dictionary["context"] == ' ':
               entry_dictionary["context"] = [(entry_dictionary["keyword"], [])]
            else:
               entry_dictionary["context"] = [(entry_dictionary["context"],[entry_dictionary["keyword"]])]
            #entry_dictionary["keyword"] = [entry_dictionary["keyword"]]
            statement_dictionary[row["statement_id"]] = entry_dictionary
         else:
            for keyword, contextlist in statement_dictionary[row['statement_id']]['context']:
                if keyword == row['context']:
                     contextlist.append(row['keyword'])
                     break
            else:
                if row['context'] == ' ':
                    statement_dictionary[row['statement_id']]['context'].append((row['keyword'], []))
                else:
                    statement_dictionary[row['statement_id']]['context'].append((row['context'], [row['keyword']]))
            # just add key word and/or context
            #statement_dictionary[row['statement_id']]["keyword"].append(row['keyword'])
            #context = row["context"]
            #if context != ' ':
            #   statement_dictionary[row['statement_id']]['context'].append((row['keyword'],context))
      print "\nSTATEMENT DICTIONARY START\n"
      pprint.pprint(statement_dictionary)
      print "\nSTATEMENT DICTIONARY END\n"
      #pprint.pprint(statement_dictionary)
      return statement_dictionary

main()
