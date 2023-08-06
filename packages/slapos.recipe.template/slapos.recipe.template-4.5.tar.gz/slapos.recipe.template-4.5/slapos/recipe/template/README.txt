Usage
=====

Getting started
---------------

You can start by a simple buildout::

    >>> write('buildout.cfg',
    ... '''
    ... [buildout]
    ... parts = template
    ...
    ... [template]
    ... recipe = slapos.recipe.template
    ... url = template.in
    ... output = template.out
    ...
    ... [section]
    ... option = value
    ... ''')

And a simple template::

    >>> write('template.in', '${section:option}')

We run buildout::

    >>> run_buildout()
    Installing template.

And the output file has been parsed by buildout itself::

    >>> cat('template.out')
    value

Full options
------------

There is two non required options:

``md5sum``
  Check the integrity of the input file.

``mode``
  Specify the filesystem permissions in octal notation.

Check file integrity
~~~~~~~~~~~~~~~~~~~~

Let's write a file template::

    >>> write('template.in', '${buildout:parts}')

Compute its MD5 sum::

    >>> from hashlib import md5
    >>> md5sum = md5(open('template.in', 'rb').read()).hexdigest()

Write the ``buildout.cfg`` using slapos.recipe.template::

    >>> write('buildout.cfg',
    ... '''
    ... [buildout]
    ... parts = template
    ...
    ... [template]
    ... recipe = slapos.recipe.template
    ... url = template.in
    ... output = template.out
    ... md5sum = ''' + md5sum + '''
    ... ''')

And run buildout, and see the result::

    >>> run_buildout()
    Uninstalling template.
    Installing template.

    >>> cat('template.out')
    template

If the md5sum doesn't match, the buildout fail::

    >>> write('buildout.cfg',
    ... '''
    ... [buildout]
    ... parts = template
    ...
    ... [template]
    ... recipe = slapos.recipe.template
    ... url = template.in
    ... output = template.out
    ... md5sum = 0123456789abcdef0123456789abcdef
    ... ''')
    >>> run_buildout()
    While:
      Installing.
      Getting section template.
      Initializing section template.
    Error: MD5 checksum mismatch for local resource at 'template.in'.


Specify filesystem permissions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can specify the mode of the written file::

    >>> write('template.in', '${buildout:installed}')

    >>> write('buildout.cfg',
    ... '''
    ... [buildout]
    ... parts = template
    ...
    ... [template]
    ... recipe = slapos.recipe.template
    ... url = template.in
    ... output = template.out
    ... mode = 0627
    ... ''')

    >>> run_buildout()
    Uninstalling template.
    Installing template.

And the generated file with have the right permissions::

    >>> import os, stat
    >>> print("0%o" % stat.S_IMODE(os.stat('template.out').st_mode))
    0627

Section dependency
------------------

You can use other part of buildout in the template. This way this parts
will be installed as dependency::

    >>> write('template.in', '${dependency:foobar}')
    >>> write('buildout.cfg', '''
    ... [buildout]
    ... parts = template
    ...
    ... [template]
    ... recipe = slapos.recipe.template
    ... url = template.in
    ... output = template.out
    ...
    ... [dependency]
    ... foobar = dependency content
    ... recipe = zc.buildout:debug
    ... ''')

    >>> run_buildout()
    Uninstalling template.
    Installing dependency.
      foobar='dependency content'
      recipe='zc.buildout:debug'
    Installing template.

This way you can get options which are computed in the ``__init__`` of
the dependent recipe.

Let's create a sample recipe modifying its option dict::

    >>> write('setup.py',
    ... '''
    ... from setuptools import setup
    ...
    ... setup(name='samplerecipe',
    ...       entry_points = {
    ...           'zc.buildout': [
    ...                'default = main:Recipe',
    ...           ],
    ...       }
    ...      )
    ... ''')
    >>> write('main.py',
    ... '''
    ... class Recipe(object):
    ...
    ...     def __init__(self, buildout, name, options):
    ...         options['data'] = 'foobar'
    ...
    ...     def install(self):
    ...         return []
    ... ''')

Let's just use ``buildout.cfg`` using this egg::

    >>> write('template.in', '${sample:data}')
    >>> write('buildout.cfg',
    ... '''
    ... [buildout]
    ... develop = .
    ... parts = template
    ...
    ... [template]
    ... recipe = slapos.recipe.template
    ... url = template.in
    ... output = template.out
    ...
    ... [sample]
    ... recipe = samplerecipe
    ... ''')
    >>> run_buildout()
    Develop: '/sample-buildout/.'
    Uninstalling template.
    Uninstalling dependency.
    Installing sample.
    Installing template.
    >>> cat('template.out')
    foobar
