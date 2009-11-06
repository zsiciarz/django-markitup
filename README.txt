===============
django-markitup
===============

Easy integration of the MarkItUp_ markup editor widget (by Jay Salvat) in
Django projects. Includes server-side support for MarkItUp!'s AJAX preview.


.. _MarkItUp: http://markitup.jaysalvat.com/

Installation
============

Install from PyPI with ``easy_install`` or ``pip``::

    pip install django-markitup

or get the `in-development version`_::

    pip install django-markitup==dev

.. _in-development version: http://bitbucket.org/carljm/django-markitup/get/tip.gz#egg=django_markitup-dev

To use django-markitup in your Django project:

    1. Add ``'markitup'`` to your ``INSTALLED_APPS`` setting.

    2. Make the contents of the ``markitup/media/markitup`` directory
       available at ``MEDIA_URL/markitup`` (or
       ``MARKITUP_MEDIA_URL/markitup``, see below).  This can be done
       by copying the files, making a symlink, or through your
       webserver configuration.

    3. If you want to use AJAX-based preview:
       
        - Add ``url(r'^markitup/', include('markitup.urls')`` in your
          root URLconf.
        - Set the MARKITUP_PREVIEW_FILTER setting (see `Using AJAX preview`_ 
          below).

Using the MarkItUp! widget
==========================

The MarkItUp! widget lives at ``markitup.widgets.MarkItUpWidget``, and
can be used like any other Django custom widget.

To assign it to a form field::

    from markitup.widgets import MarkItUpWidget
    ...
    content = forms.TextField(widget=MarkItUpWidget())

When this form is displayed on your site, you must include the form
media somewhere on the page using ``{{ form.media }}``, or the
MarkItUpWidget will have no effect.

To use MarkItUpWidget in the Django admin::

    from markitup.widgets import MarkItUpWidget
    
    class MyModelAdmin(admin.ModelAdmin):
    ...
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'content':
            kwargs['widget'] = MarkItUpWidget(attrs={'class': 'vLargeTextField'})
        return super(MyModelAdmin, self).formfield_for_dbfield(db_field, **kwargs)

You can also use the formfield_overrides attribute of the ModelAdmin, which
is simpler but only allows setting the widget per field type (so it isn't
possible to use the MarkItUpWidget on one TextField in a model and not
another)::

    from markitup.widgets import MarkItUpWidget
    
    class MyModelAdmin(admin.ModelAdmin):
        formfield_overrides = {models.TextField: {'widget': MarkItUpWidget}}

Using MarkItUp! via templates
=============================

In some cases it may be inconvenient to use ``MarkItUpWidget`` (for
instance, if the form in question is defined in third-party code). For
these cases, django-markitup provides template tags to achieve the
same effect purely in templates.

First, load the django-markitup template tag library::

    {% load markitup_tags %}

Then include the MarkItUp! CSS and Javascript in the <head> of your page::

    {% markitup_media %}

By default the ``markitup_media`` tag also includes jQuery, based on
the value of your ``JQUERY_URL`` setting, with a fallback to the
version hosted at Google Ajax APIs (see below). To suppress the
inclusion of jQuery (if you are already including it yourself), pass
any non-zero argument to the tag::

    {% markitup_media "no-jquery" %}

If you prefer to link CSS and Javascript from different locations, the
``markitup_media`` tag can be replaced with two separate tags,
``markitup_css`` and ``markitup_js``. ``markitup_js`` accepts a
parameter to suppress jQuery inclusion, just like
``markitup_media``. (Note that jQuery must be included in your
template before the ``markitup_editor`` tag is used).

Last, use the ``markitup_editor`` template tag to apply the MarkItUp!
editor to a textarea in your page. It accepts one argument, the HTML
id of the textarea. Note that if you are rendering the textarea in the
usual way via a Django form object, that id value is available as
``form.fieldname.auto_id``::

    {{ form.fieldname }}
    
    {% markitup_editor form.fieldname.auto_id %}

You can use ``markitup_editor`` on as many different textareas as you
like.

The actual HTML included by these templatetags is defined by the
contents of the templates ``markitup/include_css.html``,
``markitup/include_js.html``, and ``markitup/editor.html``. You can
override these templates in your project and customize them however
you wish.

Choosing a MarkItUp! button set and skin
========================================

MarkItUp! allows the toolbar button-set to be customized in a
Javascript settings file.  By default, django-markitup uses the
"default" set (meant for HTML editing).  Django-markitup also includes
basic "markdown" and "textile" sets (these are the sets available from
`the MarkItUp site <http://markitup.jaysalvat.com>`_, modified only to
add previewParserPath).

To use an alternate set, assign the ``MARKITUP_SET`` setting a URL
path (absolute or relative to ``MEDIA_URL``/``MARKITUP_MEDIA_URL``) to
the set directory.  For instance, to use the "markdown" set included
with django-markitup::

    MARKITUP_SET = 'markitup/sets/markdown'

MarkItUp! skins can be specified in a similar manner.  Both "simple"
and "markitup" skins are included, by default "simple" is used.  To
use the "markitup" skin instead::

    MARKITUP_SKIN = 'markitup/skins/markitup'

Neither of these settings has to refer to a location inside
django-markitup's media.  You can define your own sets and skins and
store them anywhere, as long as you set the MARKITUP_SET and
MARKITUP_SKIN settings to the appropriate URLs.

Set and skin may also be chosen on a per-widget basis by passing the
``markitup_set`` and ``markitup_skin`` keyword arguments to
MarkItUpWidget.


Using AJAX preview
==================

If you've included ``markitup.urls`` in your root URLconf (as
demonstrated above under `Installation`_), all you need to enable
server-side AJAX preview is the ``MARKITUP_PREVIEW_FILTER`` setting.

``MARKITUP_PREVIEW_FILTER`` must be a two-tuple.  

The first element must be a string, the Python dotted path to a markup
filter function.  This function should accept markup as its first
argument and return HTML.  It may accept other keyword arguments as
well.  You may parse your markup for preview using any method you
choose, as long as you can wrap it in a function that meets these
criteria.

The second element must be a dictionary of keyword arguments to pass
to the filter function.  The dictionary may be empty.

For example, if you have python-markdown installed, you could use it
like this::

    MARKITUP_PREVIEW_FILTER = ('markdown.markdown', {'safe_mode': True})

Alternatively, you could use the "textile" filter provided by Django
like this::

    MARKITUP_PREVIEW_FILTER = ('django.contrib.markup.templatetags.markup.textile', {})

(The textile filter function doesn't accept keyword arguments, so the
kwargs dictionary must be empty in this case.)

The rendered HTML content is displayed in the Ajax preview wrapped by
an HTML page generated by the ``markitup/preview.html`` template; you
can override this template in your project and customize the preview
output.

**Note:** If you use your own custom MarkItUp! set, be sure to set the
  ``previewParserPath`` option to ``'/markitup/preview/'``.


Other settings
==============

MARKITUP_MEDIA_URL
------------------

Some projects separate user-uploaded media at ``MEDIA_URL`` from
static assets. If you keep static assets at a URL other than
``MEDIA_URL``, just set ``MARKITUP_MEDIA_URL`` to that URL, and make
sure the contents of the ``markitup/media/markitup`` directory are
available at ``MARKITUP_MEDIA_URL/markitup/``.

JQUERY_URL
----------

MarkItUp! requires the jQuery Javascript library.  By default,
django-markitup links to the most recent minor version of jQuery 1.3
available at ajax.googleapis.com (via the URL
``http://ajax.googleapis.com/ajax/libs/jquery/1.3/jquery.min.js``).
If you wish to use a different version of jQuery, or host it yourself,
set the JQUERY_URL setting.  For example::

    JQUERY_URL = 'jquery.min.js'

This will use the jQuery available at MEDIA_URL/jquery.min.js. Note
that a relative ``JQUERY_URL`` is always relative to ``MEDIA_URL``, it
does not use ``MARKITUP_MEDIA_URL``.
