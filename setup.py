__doc__ = """
An easy to use app that provides Stack Overflow style badges with a minimum ammount of effort in django

See the README file for details, usage info, and a list of gotchas.
"""

from setuptools import setup

setup(
    name='resigner',
    version='0.2.1',
    author='Mediapredict',
    author_email='engineering@mediapredict.com',
    description=('Django app that provides a way to simply secure your APIs'),
    license='GPLv3',
    keywords='django api signed',
    url='https://github.com/mediapredict/resigner',
    packages=['resigner', 'resigner.migrations'],
    package_data={},
    install_requires=[
        "django >= 1.7",
        "requests >= 2.5",
    ],
    long_description=__doc__,
    classifiers=[
    	'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Framework :: Django',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities'
    ]
)
