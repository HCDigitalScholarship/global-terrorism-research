import sys
import os
import csv
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from gtr_site.models import *
import make_dictionary


class Command(BaseCommand):
   help = "Imports/updates the database"
   def add_arguments(self,parser):
      parser.add_argument("inputCSVFile",nargs=1, type=str, help="Name of file to import (include .csv)")

   def handle(self, *args, **options):
      with open('resources_loading_data.csv') as f:
         # I did this totally rad list comprehension that may be confusing
         data_dict = [{k:v for k,v in row_guy} for row_guy in [row.items() for row in csv.DictReader(f, skipinitialspace=True)] ]
         for resource in data_dict:
            Resource.objects.update_or_create(
              title = resource['title'],
              defaults = {
                'resource_type'        : resource['type'],
                'description' : resource['description'],
                'country'     : resource['country'],
                'author'      : resource['author'],
                'link'        : resource['link'],
              }
            )
