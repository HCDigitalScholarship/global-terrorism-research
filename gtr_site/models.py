from __future__ import unicode_literals
from django.contrib.auth.models import User

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

    pdf_text = models.TextField(blank=True, verbose_name='PDF text')
   
   
   
    def __str__(self):
        return self.statement_id

    def get_absolute_url(self):
        return reverse('gtr_site:statement', args=[self.statement_id])

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
    def get_solo_keywords(self):
        #iterate over all keywords with no context.
        #was edited from being named 'get_keywords' because I think that whoosh schema needs to get all keywordincontext objects assoc with a statement and other
        #files that use get_keywords (I'm pretty sure I may use it in the importer) really need to use get_solo_keywords instead.
        return self.keywords.all().filter(context=None)
    """
    def get_keywords_obj(self):
        #This is what I think whoosh_schema needs to do.
        return self.keywords.all()
    """	
    def get_keywords(self):
        #this is what I think views.py needs to do.
        mk_list = []
        for each in self.keywords.all():
           mk_list.append(each.get_main_keyword())
        return mk_list

    # returns list of unique keywords
    def get_keywords_unique(self):
        return set([keyword.get_main_keyword() for keyword in self.keywords.all()])

    """
     I'm adding these back in because I want to use them for something.
     I am confused why we needed to change them? 
        -Dylan
    """
    # returns list of keywords
    def get_keywords_obj(self):
        return set([keyword.main_keyword for keyword in self.keywords.all()])

    # makes list of contexts
    def get_contexts_obj(self):
	contexts = [keyword.context for keyword in self.keywords.all()]
	return set(contexts)

    def get_keywords_contexts_obj(self):
	"""
        key_con = {}
        for keyword in self.get_keywords_obj():
	   print "keyword:",keyword,"context:",keyword.context
	   if keyword in key_con:
		print "In models-get_keywords_contexts_obj:"
		print "This should not have happened and you should be very concerned"
	   else:
		key_con[keyword] = []
	   # for each keywordinContext that has this keyword as a main_keyword, add the context
           for KIC in KeywordInContext.objects.all().filter(main_keyword=keyword.main_keyword):
	      key_con[keyword].append(KIC.context)
	print key_con 
        return key_con
	"""
	key_con = {}
	for KIC in self.keywords.all():
            keyword = KIC.main_keyword
	    context = KIC.context
	    if keyword  not in key_con:
		key_con[keyword] = [context]
	    else:
		key_con[keyword].append(context)
	return key_con
    # makes list of contexts
    #def get_contexts(self):
        #return self.context_set.all()

    #def get_keywords_contexts(self):
        #key_con = {}
        #for keyword in self.get_keywords():
           #key_con[keyword] = keyword.context_set.filter(statement__id=self.id)
        #return key_con


    #the get_keywo
    def get_keywords_contexts(self):
        #return self.context_set.all().filter(context!=None)
        main_keyword_list = []
        keyconlist = []
        keycondict = {}
        #for keywordcontext in self.keywords.all():
           #if keywordcontext.context: #if there's a paired context
               #if keywordcontext.main_keyword not in main_keyword_list: #if the main keyword of the pair is new...
                   #main_keyword_list.append(keywordcontext.main_keyword)
               #keyconlist.append((keywordcontext.main_keyword, keywordcontext.context,))
        for keywordcontext in self.keywords.all():
            if keywordcontext.main_keyword.word == "" or keywordcontext.context.word == "":
             continue

            if not keycondict.get(keywordcontext.main_keyword.word):
                keycondict[keywordcontext.main_keyword.word] = []
           #if not keywordcontext.context or not keywordcontext.main_keyword:
              #continue
            keycondict[keywordcontext.main_keyword.word].append(keywordcontext.context.word.encode("utf-8"))
        
        return keycondict
        
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
            return self.main_keyword.word + " - " + self.context.word
        else:
            return  self.main_keyword.word
        #return self.keyword.word + ' (' + ', '.join(c.word for c in self.contexts.all()) + ')'
    def get_main_keyword(self):
        return self.main_keyword.word

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

@python_2_unicode_compatible
class List(models.Model):
    list_name = models.CharField(max_length=200, blank=True)
    #user = models.ManyToManyField(User, blank=True)
    statements = models.ManyToManyField(Statement, blank=True)
    def __str__(self):
        return self.list_name
