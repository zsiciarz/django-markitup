from __future__ import with_statement
import re
import warnings
from django.template import Template, Context, get_library
from django.test import TestCase, Client
from django.conf import settings as django_settings
from markitup import settings
from markitup.widgets import MarkItUpWidget
from django.templatetags.markitup_tags import _get_markitup_context

class PreviewTests(TestCase):
    def test_preview_filter(self):
        c = Client()
        response = c.post('/markitup/preview/',
                          {'data': 'replace this with something else'})
        self.assertContains(response, 'replacement with something else',
                            status_code=200)

    def test_preview_css(self):
        c = Client()
        response = c.post('/markitup/preview/',
                          {'data': 'replace this with something else'})
        self.assertContains(response, '/media/markitup/preview.css',
                            status_code=200)

    def test_preview_media_url(self):
        _old_miu_media_url = settings.MARKITUP_MEDIA_URL
        try:
            settings.MARKITUP_MEDIA_URL = '/some/path/'
            c = Client()
            response = c.post('/markitup/preview/',
                              {'data': 'replace this with something else'})
            self.assertContains(response, '/some/path/markitup/preview.css',
                                status_code=200)
        finally:
            settings.MARKITUP_MEDIA_URL = _old_miu_media_url

    def test_preview_template(self):
        c = Client()
        response = c.post('/markitup/preview/',
                          {'data': 'replace this with something else'})
        self.assertTemplateUsed(response, 'markitup/preview.html')


class MIUTestCase(TestCase):
    def assertIn(self, needle, haystack):
        self.failUnless(needle in haystack,
                        "'%s' not in '%s'" % (needle, haystack))

    def render(self, template_string, context_dict=None):
        """A shortcut for testing template output."""
        if context_dict is None:
            context_dict = {}

        c = Context(context_dict)
        t = Template(template_string)
        return t.render(c).strip()


class TemplatetagTests(MIUTestCase):
    def test_markitup_head_deprecation_warning(self):
        tpl_string = "{% load markitup_tags %}{% markitup_head %}"
        if hasattr(warnings, 'catch_warnings'):
            with warnings.catch_warnings(record=True) as w:
                out = self.render(tpl_string)
                # make sure it still works
                self.assertIn('jquery.markitup.js', out)
                self.assertEquals(len(w), 1)
                self.failUnless(issubclass(w[-1].category, DeprecationWarning))
        else:
            # Python < 2.6, we can't catch warnings, just test it works
            warnings.simplefilter('ignore', DeprecationWarning)
            out = self.render(tpl_string)
            warnings.resetwarnings()
            self.assertIn('jquery.markitup.js', out)

                      
class RenderTests(MIUTestCase):
    def test_widget_render(self):
        widget = MarkItUpWidget()
        self.assertIn('$("#my_id").markItUp(mySettings);',
                      widget.render('name', 'value', {'id': 'my_id'}))

    def test_templatetag_render(self):
        template = """{% load markitup_tags %}{% markitup_editor "my_id" %}"""
        self.assertIn('$("#my_id").markItUp(mySettings);',
                      self.render(template))


class TemplatetagMediaUrlTests(MIUTestCase):
    prefix = '/media'

    # helper abstractions so we can reuse same tests for widget and
    # templatetag methods
    def _reset_context(self):
        # monkeypatch a forced recalculation of the template context
        tags = get_library('django.templatetags.markitup_tags')
        tags._markitup_context = _get_markitup_context()

    multiple_newlines_re = re.compile('\n+')
        
    def _compress_newlines(self, s):
        # template includes cause extra newlines in some cases
        # where form.media always outputs only single newlines
        return self.multiple_newlines_re.sub('\n', s)
        
    def _get_media(self):
        self._reset_context()
        return self._compress_newlines(self.render("{% load markitup_tags %}{% markitup_media %}"))
    
    def _get_css(self):
        self._reset_context()
        return self.render("{% load markitup_tags %}{% markitup_css %}")
    
    def _get_js(self):
        self._reset_context()
        return self.render("{% load markitup_tags %}{% markitup_js %}")
    
    # JQUERY_URL settings and resulting link
    jquery_urls = (
        # in relative case, should always be MEDIA_URL, not MARKITUP_MEDIA_URL
        ('jquery.min.js', '/media/jquery.min.js'),
        ('some/path/jquery.min.js', '/media/some/path/jquery.min.js'),
        ('/some/path/jquery.min.js', '/some/path/jquery.min.js'),
        ('http://www.example.com/jquery.min.js', 'http://www.example.com/jquery.min.js'),
        ('https://www.example.com/jquery.min.js', 'https://www.example.com/jquery.min.js'),
        )

    # MARKITUP_SET settings and resulting CSS link
    set_urls = (
        ('some/path', '%(prefix)s/some/path/%(file)s'),
        ('some/path/', '%(prefix)s/some/path/%(file)s'),
        ('/some/path', '/some/path/%(file)s'),
        ('/some/path/', '/some/path/%(file)s'),
        ('http://www.example.com/path', 'http://www.example.com/path/%(file)s'),
        ('http://www.example.com/path/', 'http://www.example.com/path/%(file)s'),
        ('https://www.example.com/path', 'https://www.example.com/path/%(file)s'),
        ('https://www.example.com/path/', 'https://www.example.com/path/%(file)s'),
        )

    skin_urls = set_urls

    def test_all_media(self):
        out = """<link href="%(prefix)s/markitup/skins/simple/style.css" type="text/css" media="screen" rel="stylesheet" />
<link href="%(prefix)s/markitup/sets/default/style.css" type="text/css" media="screen" rel="stylesheet" />
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.3/jquery.min.js"></script>
<script type="text/javascript" src="%(prefix)s/markitup/jquery.markitup.js"></script>
<script type="text/javascript" src="%(prefix)s/markitup/sets/default/set.js"></script>""" % {'prefix': self.prefix}
        self.assertEquals(self._get_media(), out)

    def test_jquery_url(self):
        _old_jquery_url = settings.JQUERY_URL
        try:
            for url, link in self.jquery_urls:
                settings.JQUERY_URL = url
                self.assertIn(link, self._get_js())
        finally:
            settings.JQUERY_URL = _old_jquery_url
        
    def test_set_via_settings(self):
        _old_miu_set = settings.MARKITUP_SET
        try:
            for miu_set, link in self.set_urls:
                css_link = link % {'prefix': self.prefix, 'file': 'style.css'}
                js_link = link % {'prefix': self.prefix, 'file': 'set.js'}
                settings.MARKITUP_SET = miu_set
                self.assertIn(css_link, self._get_css())
                self.assertIn(js_link, self._get_js())
        finally:
            settings.MARKITUP_SET = _old_miu_set
        
    def test_skin_via_settings(self):
        _old_miu_skin = settings.MARKITUP_SKIN
        try:
            for miu_skin, link in self.skin_urls:
                link = link % {'prefix': self.prefix, 'file': 'style.css'}
                settings.MARKITUP_SKIN = miu_skin
                self.assertIn(link, self._get_css())
        finally:
            settings.MARKITUP_SKIN = _old_miu_skin


class WidgetMediaUrlTests(TemplatetagMediaUrlTests):
    def _get_media_obj(self, *args, **kwargs):
        widget = MarkItUpWidget(*args, **kwargs)
        return widget.media

    def _get_media(self, *args, **kwargs):
        return str(self._get_media_obj(*args, **kwargs))
    
    def _get_css(self, *args, **kwargs):
        return str(self._get_media_obj(*args, **kwargs)['css'])
    
    def _get_js(self, *args, **kwargs):
        return str(self._get_media_obj(*args, **kwargs)['js'])

    def test_set_via_argument(self):
        for miu_set, link in self.set_urls:
            css_link = link % {'prefix': self.prefix, 'file': 'style.css'}
            js_link = link % {'prefix': self.prefix, 'file': 'set.js'}
            self.assertIn(css_link, self._get_css(markitup_set=miu_set))
            self.assertIn(js_link, self._get_js(markitup_set=miu_set))
        
    def test_skin_via_argument(self):
        for miu_skin, link in self.skin_urls:
            link = link % {'prefix': self.prefix, 'file': 'style.css'}
            self.assertIn(link, self._get_css(markitup_skin=miu_skin))

            
class AlternateMediaUrlTests(object):
    """
    Test that MARKITUP_MEDIA_URL properly sets the prefix used for all
    MarkItUp media with relative provided URLs.

    """
    prefix = '/static'

    def setUp(self):
        self._old_miu_media_url = settings.MARKITUP_MEDIA_URL
        settings.MARKITUP_MEDIA_URL = django_settings.STATIC_URL
        
    def tearDown(self):
        settings.MARKITUP_MEDIA_URL = self._old_miu_media_url


class TemplatetagAlternateMediaUrlTests(AlternateMediaUrlTests,
                                        TemplatetagMediaUrlTests):
    pass

class WidgetAlternateMediaUrlTests(AlternateMediaUrlTests,
                                   WidgetMediaUrlTests):
    pass
