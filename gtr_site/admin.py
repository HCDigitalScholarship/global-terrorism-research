from django.contrib import admin
from gtr_site.models import *



##########################################################

class OrganizationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Organization, OrganizationAdmin) 

##########################################################

class PersonAdmin(admin.ModelAdmin):
    pass

admin.site.register(Person, PersonAdmin) 

##########################################################

class StatementAdmin(admin.ModelAdmin):
    pass

admin.site.register(Statement, StatementAdmin) 

##########################################################

class KeywordAdmin(admin.ModelAdmin):
    pass

admin.site.register(Keyword, KeywordAdmin) 

##########################################################

class ContextAdmin(admin.ModelAdmin):
    pass

admin.site.register(Context, ContextAdmin) 

##########################################################
