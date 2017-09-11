"""
Forms.py, being used primarily for autocomplete
"""

from dal import autocomplete

#from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField
#from new_bridge.reverse_related import *

from django import forms
from .models import Statement, Keyword, Context, KeywordInContext

import logging
logger = logging.getLogger("gtr_site")

from django.forms import formset_factory
from django.contrib.admin.widgets import FilteredSelectMultiple, RelatedFieldWidgetWrapper


#In order for this to work...
#A user needs to be able to select all Keywords that they want and then have a filter_horizontal field come up for that.
class KeywordInContextForm(forms.ModelForm):
    #source_keyword = forms.ModelMultipleChoiceField(
        #queryset = Keyword.objects.all(),
        #widget = autocomplete.ModelSelect2Multiple(url='keyword-autocomplete')
    #)
    main_keyword = forms.ModelChoiceField(
        queryset = Keyword.objects.all(),
        widget = autocomplete.ModelSelect2(url='keywordincontext-autocomplete'),
    )
    context = forms.ModelChoiceField(
        queryset = Keyword.objects.all(),
        widget = autocomplete.ModelSelect2(url='keywordincontext-autocomplete'),
    )
    
    class Meta:
       model = KeywordInContext
       fields = ('__all__')
       #widgets = {
        #    'main_keyword': autocomplete.ModelSelect2(url='keywordincontext-autocomplete')
       #}
   


class KeywordFilterForm(forms.ModelForm):
    class Meta:
       model = Keyword
       fields = ('__all__')
       widgets = {
            'keyword-filters': autocomplete.ModelSelect2(url='keywordfilter-autocomplete')
        }
       


class StatementForm(forms.ModelForm):
    '''statement_keywords = forms.ModelMultipleChoiceField(
       queryset = Keyword.objects.all(),
       widget = autocomplete.ModelSelect2Multiple(url='keyword-autocomplete')
    )
   
    statement_contexts = forms.ModelMultipleChoiceField(
       queryset = Context.objects.all(),
        widget=FilteredSelectMultiple(
           verbose_name="Statement Contexts Widget",
           is_stacked=False)
    )'''

    statement_keywords = forms.ModelMultipleChoiceField(
        queryset=KeywordInContext.objects.all(),
        required=False,
        label=('Select keyword context pairs that you would like to assign to this statement on the left. Hold CTRL and click to select multiple options at once. Keyword/Context pairs that are assigned to this statement are on the right.'),
        widget=FilteredSelectMultiple(
            verbose_name='Keywords Associated with Statement',
            is_stacked=False
          )
    )
    '''statement_keycons = forms.ModelMultipleChoiceField(
        queryset=KeywordInContext.objects.filter(context__isnull=False),
        required=False,
        label=('Select keyword and context pairs currently existing within the database that you would like to use'),
        widget=FilteredSelectMultiple(
            verbose_name='KeywordContextPairs Associated with Statement',
            is_stacked=False
        ),
    )'''

    class Meta:
        model = Statement
        exclude = ('keywords',)#("statement_keywords",)
        #fields = ('__all__')
        #widget= {"keyword":autocomplete.ModelSelect2Multiple(url='keyword-autocomplete')}

    #def save(self, *args, **kwargs):
     #   with open('/tmp/help.log', 'w') as fsock:
      #      fsock.write(str(self.cleaned_data))
       # return super().save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(StatementForm, self).__init__(*args, **kwargs)
        #rel = ManyToManyRel(self.instance.statement_keywords.model, 'id')
        self.fields['statement_keywords'].widget = RelatedFieldWidgetWrapper(
                                                self.fields['statement_keywords'].widget,
                                                Statement._meta.get_field('keywords').rel,
                                                self.admin_site) 
        if self.instance.pk:
           self.fields['statement_keywords'].initial = self.instance.keywords.all()#_set.all() #parse whaat this line is doing.
           #self.fields['statement_keywords'].widget = RelatedFieldWidgetWrapper(self.fields['statement_keywords'].widget, rel, self.admin_site)

    def save(self, commit=True):
        statement = super(StatementForm, self).save(commit=False)  
        if commit:
            statement.save()
        if statement.pk:
            statement.keywords_set = self.cleaned_data['keywords'] #change to keyword if need be
            self.save_m2m()

        return statement

'''class SearchByDateForm(forms.Form):
    date_to_edit = forms.DateField(input_formats=['%m/%d/%Y'],
                                   widget=forms.TextInput(attrs={
                                        'class': 'form-control',
                                        'id': 'trips_month'}),
                                   initial=date.strftime(date.today(),
                                                         '%m/%d/%Y'))'''



    #def is_valid(self, *args, **kwargs):
	#logger.debug('Bad: %s', str(self.data))
        #return super(StatementForm, self).is_valid(*args, **kwargs)

#accu=0
#StatementFormSet = formset_factory(StatementForm)
#for form in StatementFormSet:
#    logger.debug(form)

#logger.debug("accu value: " + str(accu))


#class KeywordForm(forms.ModelForm):
    #statement = AutoCompleteSelectMultipleField('statement')
    #class Meta:
       #model = Keyword
       #fields = '__all__'
    #statement =  AutoCompleteSelectMultipleField('statement')
    #exclude = ('statement')
