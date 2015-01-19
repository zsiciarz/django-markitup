import posixpath

from django.contrib.staticfiles.storage import FileSystemStorage


class SomeCustomStorage(FileSystemStorage):
    def url(self, name):
        return posixpath.join('https://cdn.example.com/static', name)
