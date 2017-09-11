#lookup channel file for the gtr. Delete if not working.

from ajax_select import register, LookupChannel
from .models import *
#from permissionz import permissions


@register('keyword')
def KeywordLookup(LookupChannel):
    model = Keyword

    #def can_add(self, user, model):
     # return permissions.has_perm('can_add', model, user)
    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q).order_by('name')[:50]

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.name

