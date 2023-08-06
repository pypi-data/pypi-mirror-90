from string import Template

from django.template import Library
from django.utils.timesince import timesince


register = Library()


class DeltaTemplate(Template):
    delimiter = "%"


@register.simple_tag
def timedelta(d1, d2, precision=None):
    if precision is None:
        precision = 6
    tdelta = d1 - d2
    s = str(tdelta)
    if precision <= 0 or '.' not in s:
        return s.split('.')[0]
    return s.split('.')[0] + '.' + s.split('.')[1][0:precision]
