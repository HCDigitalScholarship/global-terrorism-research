from django.contrib import admin
from gtr_site.models import *
from .forms import StatementForm



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
    class Media():
        js = ('gtr_site/js/filtering.js',)
    form = StatementForm
    exclude = ("statement_keywords", "statement_contexts",)

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

class ResourceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Resource, ResourceAdmin) 

##########################################################

class PairAdmin(admin.ModelAdmin):
    pass

admin.site.register(KeyConPairs, PairAdmin)
##########################################################
