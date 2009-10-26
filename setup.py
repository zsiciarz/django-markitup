from setuptools import setup, find_packages
 
setup(
    name='django-markitup',
    version='0.2.10dev',
    description='Django integration with the MarkItUp universal markup editor',
    long_description=open('README.txt').read(),
    author='Carl Meyer',
    author_email='carl@dirtcircle.com',
    url='http://bitbucket.org/carljm/django-markitup/',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    zip_safe=False,
    package_data={'markitup': ['templates/markitup/*.html',
                               'media/markitup/*.*',
                               'media/markitup/sets/*/*.*',
                               'media/markitup/sets/*/images/*.png',
                               'media/markitup/skins/*/*.*',
                               'media/markitup/skins/*/images/*.png',
                               'media/markitup/templates/*.*']}
)
