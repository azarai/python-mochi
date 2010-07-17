"""
python-mochi
------------

python-mochi is a lib for working with the `mochiads api <https://www.mochimedia.com/support/pub_docs>`_


Links
`````

* `website <http://codeboje.de/python-mochi/>`_
* `development version
  <http://github.com/azarai/python-mochi>`_

"""
from distutils.core import setup

setup(name="python-mochi",
      version="0.0.1",
      description="A Python lib for the mochiads api",
      long_description=__doc__,
      author="Jens Boje",
      author_email="hello@codeboje.de",
      url="http://codeboje.de/python-mochi/",
      packages=['mochi'],
      platforms='any',
      license = 'BSD',
      classifiers = [
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
          'Topic :: Software Development :: Libraries :: Python Modules'
          ],
     )
