"""
 * Keyword script that makes a basic json
 *  object in the format of [ { id : int, name: keyword}, {...}  ]
 *  for every keyword. This is in conjunction with the following plugin script
 *
 *
 *
"""
import sys
import os
from gtr_site.models import *
import json

def main():
   i = 1
   pythondictionary = []
   for each in Keyword.objects.all():
      pythondictionary.append({'id' : i, 'name' : each.word})
      i+=1

   jsondict = json.dumps(pythondictionary)
   print jsondict
   return jsondict



main()

