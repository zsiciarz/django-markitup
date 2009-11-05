from django.test import TestCase
from django.core import serializers
from django.forms.models import modelform_factory
from django.contrib import admin
from markitup.fields import MarkupField
from markitup.widgets import MarkupTextarea, AdminMarkItUpWidget
from markitup.tests.models import Post

def test_filter(text, **kwargs):
    return unicode(text) + unicode(kwargs)

class MarkupFieldTests(TestCase):
    def setUp(self):
        self.post = Post.objects.create(title='example post',
                                        body='**markdown**')

    def testUnicodeRender(self):
        self.assertEquals(unicode(self.post.body),
                          u'<p><strong>markdown</strong></p>')

    def testRaw(self):
        self.assertEquals(self.post.body.raw, '**markdown**')

    def testRendered(self):
        self.assertEquals(self.post.body.rendered,
                          u'<p><strong>markdown</strong></p>')

    def testLoadBack(self):
        post = Post.objects.get(pk=self.post.pk)
        self.assertEquals(post.body.raw, self.post.body.raw)
        self.assertEquals(post.body.rendered, self.post.body.rendered)

    def testAssignToBody(self):
        self.post.body = '*different markdown*'
        self.post.save()
        self.assertEquals(unicode(self.post.body),
                          u'<p><em>different markdown</em></p>')

    def testAssignToRaw(self):
        self.post.body.raw = '*more markdown*'
        self.post.save()
        self.assertEquals(unicode(self.post.body),
                          u'<p><em>more markdown</em></p>')

    def testAssignToRendered(self):
        def _invalid_assignment():
            self.post.body.rendered = 'this should fail'
        self.assertRaises(AttributeError, _invalid_assignment)

# TODO
#    def testOverrideFilter(self):
#        self.post.body.save_markup('markitup.tests.tests.test_filter',
#                                   some_arg='some_val')
#        self.assertEquals(unicode(self.post.body),
#                          u"**markdown**{'some_arg': 'some_val'}")


class MarkupFieldSerializationTests(TestCase):
    def setUp(self):
        self.post = Post.objects.create(title='example post',
                                        body='**markdown**')
        self.stream = serializers.serialize('json', Post.objects.all())

    def testSerializeJSON(self):
        self.assertEquals(self.stream,
                          '[{"pk": 1, "model": "tests.post", '
                          '"fields": {"body": "**markdown**", '
                          '"_body_rendered": "<p><strong>markdown</strong></p>", '
                          '"title": "example post"}}]')

    def testDeserialize(self):
        self.assertEquals(list(serializers.deserialize("json",
                                                       self.stream))[0].object,
                          self.post)


class MarkupFieldFormTests(TestCase):
    def setUp(self):
        self.post = Post(title='example post', body='**markdown**')
        self.form_class = modelform_factory(Post)

    def testWidget(self):
        self.assertEquals(self.form_class().fields['body'].widget.__class__,
                          MarkupTextarea)

    def testFormFieldContents(self):
        form = self.form_class(instance=self.post)
        self.assertEquals(unicode(form['body']),
                          u'<textarea id="id_body" rows="10" cols="40" name="body">**markdown**</textarea>')

    def testAdminFormField(self):
        ma = admin.ModelAdmin(Post, admin.site)
        self.assertEquals(ma.formfield_for_dbfield(
                Post._meta.get_field('body')).widget.__class__,
                          AdminMarkItUpWidget)
