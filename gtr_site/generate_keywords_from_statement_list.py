"""
Functions currently used in basic_search.py and filtering.py pertaining to getting the right keywords for display.

"""
from models import *
import time

def generate_keywords_dictionary(statement_list):
    """
       given a list of statement (like the one returned when you query the DB)
       find all the keywords linked to those statements and the number of time the are linked
       return a dictionary where keys are keywords and values are that number:  {Iraq : 300}
    """

    start = time.time()
    keywords_dict = {}
    for statement in statement_list:
        for keyword in statement.get_keywords():
            if keyword in keywords_dict:
                keywords_dict[keyword]+=1
            else:
                keywords_dict[keyword] = 1

    print "generating keywords took", time.time() - start, "seconds"
    return keywords_dict


def get_top_keywords(keywords_dict, top_n):
    """
    Used to get the top results to display for keyword filtering

    Given a dictionary of keywords as keys and the number of times that keyword is linked to a statement in the search results: {Iraq : 300}
    Returns the top n results as as list of pairs, ordered by appearances: [(Iraq, 300), (Iran, 200)]
    """
    return sorted(keywords_dict.items(), key=lambda student: student[1], reverse=True)[:top_n]


    
def generate_top_n_keywords(statement_list, top_n):
    """
     Generates and gets top n keywords.
    """
    return get_top_keywords(generate_keywords_dictionary(statement_list), top_n)

def generate_just_keywords(statement_list):
    """
       You might need this and I already wrote it! Returns a set of keywords
    """
    start = time.time()
    keywords = set()
    keyword_sets = [set(statement.get_keywords()) for statement in qs_list]
    keywords = keywords.union(*keyword_sets)
    print "generating keywords took", time.time() - start, "seconds"
    return keywords
