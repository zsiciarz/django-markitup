from django.conf import settings
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.functional import curry
from django.core.exceptions import ImproperlyConfigured
from markitup import widgets

_rendered_field_name = lambda name: '_%s_rendered' % name

def _get_render_func(dotted_path, **kwargs):
    (module, func) = dotted_path.rsplit('.', 1)
    func = getattr(__import__(module, {}, {}, [func]), func)
    return curry(func, **kwargs)

try:
    render_func = _get_render_func(settings.MARKITUP_FILTER[0],
                                   **settings.MARKITUP_FILTER[1])
except ImportError, e:
    raise ImproperlyConfigured("Could not import MARKITUP_FILTER %s: %s" %
                               (settings.MARKITUP_FILTER, e))
except AttributeError, e:
    raise ImproperlyConfigured("MARKITUP_FILTER setting is required")

class Markup(object):
    def __init__(self, instance, field_name, rendered_field_name):
        # instead of storing actual values store a reference to the instance
        # along with field names, this makes assignment possible
        self.instance = instance
        self.field_name = field_name
        self.rendered_field_name = rendered_field_name

    # raw is read/write
    def _get_raw(self):
        return self.instance.__dict__[self.field_name]
    def _set_raw(self, val):
        setattr(self.instance, self.field_name, val)
    raw = property(_get_raw, _set_raw)

    # rendered is a read only property
    def _get_rendered(self):
        return getattr(self.instance, self.rendered_field_name)
    rendered = property(_get_rendered)

    # allows display via templates to work without safe filter
    def __unicode__(self):
        return mark_safe(self.rendered)

class MarkupDescriptor(object):
    def __init__(self, field):
        self.field = field
        self.rendered_field_name = _rendered_field_name(self.field.name)

    def __get__(self, instance, owner):
        if instance is None:
            raise AttributeError('Can only be accessed via an instance.')
        markup = instance.__dict__[self.field.name]
        if markup is None:
            return None
        return Markup(instance, self.field.name, self.rendered_field_name)

    def __set__(self, obj, value):
        if isinstance(value, Markup):
            obj.__dict__[self.field.name] = value.raw
            setattr(obj, self.rendered_field_name, value.rendered)
        else:
            obj.__dict__[self.field.name] = value

class MarkupField(models.TextField):
    def contribute_to_class(self, cls, name):
        rendered_field = models.TextField(editable=False)
        rendered_field.creation_counter = self.creation_counter+1
        cls.add_to_class(_rendered_field_name(name), rendered_field)
        super(MarkupField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, MarkupDescriptor(self))

    def pre_save(self, model_instance, add):
        value = super(MarkupField, self).pre_save(model_instance, add)
        rendered = render_func(value.raw)
        setattr(model_instance, _rendered_field_name(self.attname), rendered)
        return value.raw

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return value.raw

    def get_db_prep_value(self, value):
        try:
            return value.raw
        except AttributeError:
            return value

    def formfield(self, **kwargs):
        defaults = {'widget': widgets.MarkupTextarea}
        defaults.update(kwargs)
        return super(MarkupField, self).formfield(**defaults)

# register MarkupField to use the custom widget in the Admin
from django.contrib.admin.options import FORMFIELD_FOR_DBFIELD_DEFAULTS
FORMFIELD_FOR_DBFIELD_DEFAULTS[MarkupField] = {'widget': widgets.AdminMarkItUpWidget}
