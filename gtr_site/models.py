from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

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
    issue_date = models.DateField()
    author = models.ForeignKey(Person)
    released_by = models.ForeignKey(Organization)
    


  
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
    def __str__(self):
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

	# this was a bad way of doing this, but I had a different goal at time
	# get_keywords_contexts does what this was trying to do, but better
	"""
	contexts = []
	for keyword in self.get_keywords():
           contexts.append(keyword.context_set.filter(statement__id=self.id))
        return contexts
	"""

    def get_keywords_contexts(self):
	key_con = {}
        for keyword in self.get_keywords():
           key_con[keyword] = keyword.context_set.filter(statement__id=self.id)
        return key_con

    
# key words have statements

@python_2_unicode_compatible
class Keyword(models.Model):
    word      = models.CharField(max_length=200)
    statement = models.ManyToManyField(Statement)
    def __str__(self):
        return self.word

@python_2_unicode_compatible
class Context(models.Model):
    context_word  = models.CharField(max_length=200)
    keyword       = models.ManyToManyField(Keyword)
    statement     = models.ManyToManyField(Statement)
    def __str__(self):
        return self.context_word
    
