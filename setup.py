from setuptools import setup, find_packages
 
setup(
    name='django-markitup',
    version='0.2.5',
    description='Django integration with the MarkItUp universal markup editor',
    long_description=open('README.txt').read(),
    author='Carl Meyer',
    author_email='carl@dirtcircle.com',
    url='http://launchpad.net/django-markitup',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    package_data= {'': ['*.txt', '*.css', '*.png', '*.js', '*.html']},
    zip_safe=False,
)
