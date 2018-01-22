from django.contrib import admin
from gtr_site.models import *
from .forms import StatementForm, KeywordInContextForm
from django.utils.translation import gettext_lazy as _
from datetime import date

from django.contrib.flatpages.models import FlatPage

# Note: we are renaming the original Admin and Form as we import them!
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld
from django.contrib.flatpages.admin import FlatpageForm as FlatpageFormOld

from django import forms
from ckeditor.widgets import CKEditorWidget

class FlatpageForm(FlatpageFormOld):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
    	fields = '__all__'
    	model = FlatPage # this is not automatically inherited from FlatpageFormOld


class FlatPageAdmin(FlatPageAdminOld):
    form = FlatpageForm


# We have to unregister the normal admin, and then reregister ours
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)

##########################################################

class OrganizationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Organization, OrganizationAdmin) 

##########################################################

class PersonAdmin(admin.ModelAdmin):
    pass

admin.site.register(Person, PersonAdmin) 

##########################################################

#class KeywordInline(admin.TabularInline):
    #filter_horizontal = ('statement',)
    #model = Keyword.statement.through
    #extra = 2
    #max_num = 1
    #def has_add_permission():
       #return True
    #filter_horizontal = ('keyword_word',)
    #def media():
        #filter_horizontal = ('keyword',)
    
class KeywordAdmin(admin.ModelAdmin):
    pass
    #inlines = [KeywordInline,]
    #form = KeywordForm
    #filter_horizontal = ('statement',)
    #inlines = [KeywordInline,] 

class StatementListFilter(admin.SimpleListFilter):
    title = _('issue_date')
    parameter_name = 'decade'
    def lookups(self, request, StatementAdmin):
        return (
         #('70s', _('in the 70s'),),
         #('80s', _('in the 80s'),),
         ('90s', _('in the 90s'),),
         ('00s', _('in the 2000s'),),
         ('10s', _('in the 2010s'),),
        )
    def queryset(self, request, queryset):
       #if self.value() == '70s':
           # return queryset.filter(issue_date__gte=date(1970, 1, 1),
          #                         issue_date__lte=date(1979, 12, 31))
       #if self.value() == '80s':
            #return Statement.objects.all().filter(issue_date__gte=date(1980, 1, 1),
             #                      issue_date__lte=date(1989, 12, 31))
       if self.value() == '90s':
            return Statement.objects.all().filter(issue_date__gte=date(1990, 1, 1),
                                   issue_date__lte=date(1999, 12, 31))
       if self.value() == '00s':
            return Statement.objects.all().filter(issue_date__gte=date(2000, 1, 1),
                                   issue_date__lte=date(2009, 12, 31))
       if self.value() == '10s':
            return Statement.objects.all().filter(issue_date__gte=date(2010, 1, 1,),
                                   issue_date__lte=date(2019, 12, 31))

class KeywordInContextInline(admin.TabularInline):
      #model = Statement.keywords.through
      model = Statement.keywords.through
      #fields = ('main_keyword', 'context',)


class StatementAdmin(admin.ModelAdmin):
    list_display = ('statement_id', 'title', 'author', 'released_by', 'issue_date', 'access', 'full_text',)
    #list_filter = ('released_by', 'issue_date', 'access',)
    list_filter = (StatementListFilter, 'released_by', 'issue_date', 'access',)
    search_fields = ('statement_id', 'title', 'author__person_name', 'issue_date',)
    #search_fields = ('statement_id',)
    #search_fields = ('statement_id', 'title', 'author')
    
    form = StatementForm
    def __init__(self, model, admin_site):
        super(StatementAdmin,self).__init__(model,admin_site)
        self.form.admin_site = admin_site 
    #inlines = [KeywordInContextInline,]
    #filter_horizontal = ('keywords,')
    #exclude = ('statement',)
     #class Media():
        #js = ('gtr_site/js/filtering.js',)
    #form = StatementForm
    #exclude = ("statement_keywords")
    #filter_horizontal = ('solokeywords',)

admin.site.register(Statement, StatementAdmin) 

#########################################################
admin.site.register(Keyword, KeywordAdmin) 


##########################################################
class ResourceAdmin(admin.ModelAdmin):
    search_fields = ('title', 'country', 'author')
    list_display = ('title', 'author', 'country', 'resource_type', 'description',)
    list_filter = ('resource_type',)

admin.site.register(Resource, ResourceAdmin) 

##########################################################

class KeywordInContextAdmin(admin.ModelAdmin):
     form = KeywordInContextForm
     list_display = ('main_keyword', 'context',)
     search_fields = ('main_keyword__word', 'context__word')
     class Media():
        js = ('gtr_site/js/filtering.js',)
     #filter_horizontal = ('main_keyword', 'context')

admin.site.register(KeywordInContext, KeywordInContextAdmin)
