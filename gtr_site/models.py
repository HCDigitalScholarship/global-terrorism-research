from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.urls import reverse

@python_2_unicode_compatible
class Organization(models.Model):
    org_name = models.CharField(max_length=200)

    def __str__(self):
        return self.org_name

@python_2_unicode_compatible
class Person(models.Model):
    person_name = models.CharField(max_length=200) 

    def __str__(self):
        return self.person_name
    def __unicode__(self):
        return u'%s' % (self.person_name)

@python_2_unicode_compatible
class Statement(models.Model):
    statement_id = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    issue_date = models.DateField("Issue-Date") #"Issue-Date"
    author = models.ForeignKey(Person)
    released_by = models.ForeignKey(Organization)
    keywords = models.ManyToManyField('KeywordInContext')
   #the way to solve this issue is by making the statements have a respective key and context collection. How can we do that?

  
    ################ Media start ####################
    TEXT  = 'TX'
    AUDIO = 'AU'
    VIDEO = 'VD'
    TWEET = 'TW'

    MEDIA_TYPES = (
      (TEXT , "Text"),
      (AUDIO, "Audio"),
      (VIDEO, "Video"),
      (TWEET, "Tweet"),
    )

    media_type  = models.CharField(
        max_length=2,
        choices=MEDIA_TYPES,
        default=TEXT,
    )
    ##############    Media end    ##################
    full_text = models.URLField(blank=True, null=True)
 
    ALLUSERS = 'AL'
    HCONLY = 'HC'
    ACCESS = (
       (ALLUSERS, "All Users"),
       (HCONLY, "Haverford Users only")
    )

    access = models.CharField(
       max_length=2,
       choices=ACCESS,
       default=ALLUSERS,
    )
   
   
   
    def __str__(self):
        return self.statement_id

    def get_absolute_url(self):
        return reverse('statement', args=[self.statement_id])

    def show(self):
        info = []
	for field in Statement._meta.fields:
            if field.name == 'author':
                # This is a super unsatisfactory solution
                # I would like to find a better field property
                foreign_key =int( field.value_to_string(self))
                info.append((field.name, Person.objects.get(id=foreign_key).person_name))
	    elif field.name == 'released_by':
		foreign_key =int( field.value_to_string(self))
                info.append((field.name, Organization.objects.get(id=foreign_key).org_name))

                 
            else:
		info.append((field.name, field.value_to_string(self))) 
        return info

    # returns list of keywords
    def get_keywords(self):
        #iterate over all keywords with no context.
        return self.keywords_set.all().filter(context=None)

    # makes list of contexts
    #def get_contexts(self):
        #return self.context_set.all()

    #def get_keywords_contexts(self):
        #key_con = {}
        #for keyword in self.get_keywords():
           #key_con[keyword] = keyword.context_set.filter(statement__id=self.id)
        #return key_con
    def get_keywords_contexts(self):
        #return self.context_set.all().filter(context!=None)
        keyconlist = []
        for keywordcontext in self.keywords.all():
           if keywordcontext.context:
               keyconlist.append(keywordcontext)
        return keyconlist                 

@python_2_unicode_compatible
class Keyword(models.Model):
    word      = models.CharField(max_length=200, blank=True)
    #statement = models.ManyToManyField(Statement)
    def __str__(self):
        return self.word
    def create_keyword(cls, new_keyword):
        new_keyword = cls(new_keyword)
        return new_keyword

@python_2_unicode_compatible
class KeywordInContext(models.Model):
    main_keyword = models.ForeignKey(Keyword)
    #contexts = models.ManyToManyField(Keyword, related_name='keyword_context',)
    context = models.ForeignKey(Keyword, related_name='keyword_context', blank=True, null=True)

    def __str__(self):
        if self.context:
            return 'KEYWORD: ' + self.main_keyword.word + ' CONTEXT: ' + self.context.word
        else:
            return 'KEYWORD: ' +  self.main_keyword.word  + ' (no context)'
        #return self.keyword.word + ' (' + ', '.join(c.word for c in self.contexts.all()) + ')'

@python_2_unicode_compatible
class Context(models.Model):
    context_word  = models.CharField(max_length=200)
    keyword       = models.ManyToManyField(Keyword)
    statement = models.ManyToManyField(Statement)
    def __str__(self):
        return self.context_word #+ " (" + ", ".join(unicode(k) for k in self.keyword.all()) + ")"
    
@python_2_unicode_compatible
class Resource(models.Model):
 # might want to add choices to this
    resource_type = models.CharField(max_length=200, blank=True, null=True)
    title         = models.CharField(max_length=200, blank=True, null=True)
    description   = models.TextField(blank=True, null=True)
    country       = models.CharField(max_length=200, blank=True, null=True)
    author        = models.CharField(max_length=200, blank=True, null=True)
    link          = models.URLField(blank=True, null=True)
    def __str__(self):
        return self.title
"""
@python_2_unicode_compatible
class Statement(models.Model):
    statement_id = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    issue_date = models.DateField(blank=True)
    author = models.ForeignKey(Person)
    released_by = models.ForeignKey(Organization)
    #the way to solve this issue is by making the statements have a respective key and context collection. How can we do that?


    ################ Media start ####################
    TEXT  = 'TX'
    AUDIO = 'AU'
    VIDEO = 'VD'

    MEDIA_TYPES = (
      (TEXT , "Text"),
      (AUDIO, "Audio"),
      (VIDEO, "Video")
    )

    media_type  = models.CharField(
        max_length=2,
        choices=MEDIA_TYPES,
        default=TEXT,
    )
    ##############    Media end    ##################
    full_text = models.URLField()
    #statement_keywords = Keyword.objects.filter(
    statement_keywords = models.ManyToManyField(Keyword)
    statement_contexts = models.ManyToManyField(Context) #added blank=True fields for them. Not done before. dunno why.
    #define a custom form for model. """

"""    ALLUSERS = 'AL'
    HCONLY = 'HC'
    ACCESS = (
       (ALLUSERS, "All Users"),
       (HCONLY, "Haverford Users only")
    )

    access = models.CharField(
       max_length=2,
       choices=ACCESS,
       default=ALLUSERS,
    )"""



"""    def __str__(self):
        return self.statement_id
    def show(self):
        info = []
        for field in Statement._meta.fields:
            if field.name == 'author':
                # This is a super unsatisfactory solution
                # I would like to find a better field property
                foreign_key =int( field.value_to_string(self))
                info.append((field.name, Person.objects.get(id=foreign_key).person_name))
            elif field.name == 'released_by':
                foreign_key =int( field.value_to_string(self))
                info.append((field.name, Organization.objects.get(id=foreign_key).org_name))


            else:
                info.append((field.name, field.value_to_string(self)))
        return info
        # return [(field.name, field.value_to_string(self)) for field in Statement._meta.fields]

    # returns list of keywords
    def get_keywords(self):
        return self.keyword_set.all()

    # makes list of contexts
    def get_contexts(self):
        return self.context_set.all()

    def get_keywords_contexts(self):
        key_con = {}
        for keyword in self.get_keywords():
           key_con[keyword] = keyword.context_set.filter(statement__id=self.id)
        return key_con"""
