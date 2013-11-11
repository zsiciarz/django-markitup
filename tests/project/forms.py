from django import forms

from markitup.widgets import MarkItUpWidget


class DemoForm(forms.Form):
    content = forms.CharField(widget=MarkItUpWidget(auto_preview=True))
