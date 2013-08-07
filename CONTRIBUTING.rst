Contributing
============

Thanks for your interest in contributing to ``django-markitup``!

The code lives at https://bitbucket.org/carljm/django-markitup with a mirror at
https://github.com/carljm/django-markitup - pull requests can be submitted to
either repository.

Features and bugfixes that involve modifying Python code should be accompanied
by tests in ``tests/tests.py``, and all existing and new tests should pass. To
run tests on the full matrix of all supported Python and Django versions, ``pip
install tox`` and then run ``tox``. This requires that you have ``python2.6``
and ``python2.7`` available on your system; if you don't have one or the other,
the tests for that Python version will fail. Please note in your pull request
what version(s) of Python you successfully ran the tests with.

If your change is a new feature or has user-facing impact, please modify or add
to the documentation in ``README.rst`` as needed.

The bundled MarkItUp! JS lib ``markitup/static/markitup/jquery.markitup.js``
and the toolbar sets in ``markitup/static/markitup/sets`` are bundled directly
from upstream at http://markitup.jaysalvat.com/downloads/. Pull requests to
update to more recent code from upstream are welcome, but please do not submit
pull requests with other changes to these files; I don't want to take on
responsibility for maintaining forked versions.

Feel free to add your name to ``AUTHORS.rst`` (alphabetical order) and
summarize your change with a brief entry in ``CHANGES.rst`` as part of your
pull request.
