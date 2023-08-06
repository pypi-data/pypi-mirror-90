Jinja2 usage
============

Getting started
---------------

Example buildout demonstrating some types::

    >>> write('buildout.cfg',
    ... '''
    ... [buildout]
    ... parts = template
    ...
    ... [template]
    ... recipe = slapos.recipe.template:jinja2
    ... template = foo.in
    ... rendered = foo
    ... context =
    ...     key     bar          section:key
    ...     key     recipe       :recipe
    ...     raw     knight       Ni !
    ...     import  json_module  json
    ...     section param_dict   parameter-collection
    ...
    ... [parameter-collection]
    ... foo = 1
    ... bar = bar
    ...
    ... [section]
    ... key = value
    ... ''')

And according Jinja2 template (kept simple, control structures are possible)::

    >>> write('foo.in',
    ...     '{{bar}}\n'
    ...     'Knights who say "{{knight}}"\n'
    ...     '${this:is_literal}\n'
    ...     '${foo:{{bar}}}\n'
    ...     'swallow: {{ json_module.dumps(("african", "european")) }}\n'
    ...     'parameters from section: {{ param_dict | dictsort }}\n'
    ...     'Rendered with {{recipe}}\n'
    ...     'UTF-8 text: привет мир!\n'
    ...     'Unicode text: {{ "你好世界" }}\n'
    ... )

We run buildout::

    >>> run_buildout()
    Installing template.

And the template has been rendered::

    >>> cat('foo')
    value
    Knights who say "Ni !"
    ${this:is_literal}
    ${foo:value}
    swallow: ["african", "european"]
    parameters from section: [('bar', 'bar'), ('foo', '1')]
    Rendered with slapos.recipe.template:jinja2
    UTF-8 text: привет мир!
    Unicode text: 你好世界

Parameters
----------

Mandatory:

``template``
  Template url/path, as accepted by zc.buildout.download.Download.__call__ .
  For very short template, it can make sense to put it directly into
  buildout.cfg: the value is the template itself, prefixed by the string
  "inline:" + an optional newline.

``rendered``
  Where rendered template should be stored.

Optional:

``context``
  Jinja2 context specification, one variable per line, with 3
  whitespace-separated parts: type, name and expression. Available types are
  described below. "name" is the variable name to declare. Expression semantic
  varies depending on the type.

  Available types:

  ``raw``
    Immediate literal string.

  ``key``
    Indirect literal string.

  ``import``
    Import a python module.

  ``section``
    Make a whole buildout section available to template, as a dictionary.

  Indirection targets are specified as: [section]:key .
  It is possible to use buildout's buit-in variable replacement instead instead
  of ``key`` type, but keep in mind that different lines are different
  variables for this recipe. It might be what you want (factorising context
  chunk declarations), otherwise you should use indirect types.

``md5sum``
  Template's MD5, for file integrity checking. By default, no integrity check
  is done.

``mode``
  Mode, in octal representation (no need for 0-prefix) to set output file to.
  This is applied before storing anything in output file.

``once``
  Path of a marker file to prevents rendering altogether.

``extensions``
  Jinja2 extensions to enable when rendering the template,
  whitespace-separated. By default, none is loaded.

``import-delimiter``
  Delimiter character for in-temlate imports.
  Defaults to ``/``.
  See also: import-list

``import-list``
  Declares a list of import paths. Format is similar to ``context``.
  "name" becomes import's base name.

  Available types:

  ``rawfile``
    Literal path of a file.

  ``file``
    Indirect path of a file.

  ``rawfolder``
    Literal path of a folder. Any file in such folder can be imported.

  ``folder``
    Indirect path of a folder. Any file in such folder can be imported.

``encoding``
  Encoding for input template and output file.
  Defaults to ``utf-8``.

FAQ
---

Q: How do I generate ${foo:bar} where foo comes from a variable ?

A: ``{{ '${' ~ foo_var ~ ':bar}' }}``
   This is required as jinja2 fails parsing "${{{ foo_var }}:bar}". Though,
   jinja2 succeeds at parsing "${foo:{{ bar_var }}}" so this trick isn't
   needed for that case.

Use jinja2 extensions
~~~~~~~~~~~~~~~~~~~~~

    >>> write('foo.in',
    ... '''{% set foo = ['foo'] -%}
    ... {% do foo.append(bar) -%}
    ... {{ foo | join(', ') }}''')
    >>> write('buildout.cfg',
    ... '''
    ... [buildout]
    ... parts = template
    ...
    ... [template]
    ... recipe = slapos.recipe.template:jinja2
    ... template = foo.in
    ... rendered = foo
    ... context = key bar buildout:parts
    ... # We don't actually use all those extensions in this minimal example.
    ... extensions = jinja2.ext.do jinja2.ext.loopcontrols
    ...   jinja2.ext.with_
    ... ''')
    >>> run_buildout()
    Uninstalling template.
    Installing template.

    >>> cat('foo')
    foo, template

Check file integrity
~~~~~~~~~~~~~~~~~~~~

Compute template's MD5 sum::

    >>> write('foo.in', '{{bar}}')
    >>> from hashlib import md5
    >>> with open('foo.in', 'rb') as f:
    ...     md5sum = md5(f.read()).hexdigest()
    >>> write('buildout.cfg',
    ... '''
    ... [buildout]
    ... parts = template
    ...
    ... [template]
    ... recipe = slapos.recipe.template:jinja2
    ... template = foo.in
    ... rendered = foo
    ... context = key bar buildout:parts
    ... md5sum = ''' + md5sum + '''
    ... ''')
    >>> run_buildout()
    Uninstalling template.
    Installing template.

    >>> cat('foo')
    template

If the md5sum doesn't match, the buildout fail::

    >>> write('buildout.cfg',
    ... '''
    ... [buildout]
    ... parts = template
    ...
    ... [template]
    ... recipe = slapos.recipe.template:jinja2
    ... template = foo.in
    ... rendered = foo
    ... context = key bar buildout:parts
    ... md5sum = 0123456789abcdef0123456789abcdef
    ... ''')
    >>> run_buildout()
    Uninstalling template.
    Installing template.
    While:
      Installing template.
    Error: MD5 checksum mismatch for local resource at 'foo.in'.


Specify filesystem permissions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can specify the mode for rendered file::

    >>> write('template.in', '{{bar}}')
    >>> write('buildout.cfg',
    ... '''
    ... [buildout]
    ... parts = template
    ...
    ... [template]
    ... recipe = slapos.recipe.template:jinja2
    ... template = template.in
    ... rendered = foo
    ... context = key bar buildout:parts
    ... mode = 205
    ... ''')
    >>> run_buildout()
    Installing template.

And the generated file with have the right permissions::

    >>> import os, stat
    >>> print("0%o" % stat.S_IMODE(os.stat('foo').st_mode))
    0205

Note that Buildout will not allow you to have write permission for others
and will silently remove it (i.e a 207 mode will become 205).

Template imports
~~~~~~~~~~~~~~~~

Here is a simple template importing an equaly-simple library:

    >>> write('template.in', '''
    ... {%- import "library" as library -%}
    ... {{ library.foo() }}
    ... ''')
    >>> write('library.in', '{% macro foo() %}FOO !{% endmacro %}')

To import a template from rendered template, you need to specify what can be
imported::

    >>> write('buildout.cfg', '''
    ... [buildout]
    ... parts = template
    ...
    ... [template]
    ... recipe = slapos.recipe.template:jinja2
    ... template = template.in
    ... rendered = bar
    ... import-list = rawfile library library.in
    ... ''')
    >>> run_buildout()
    Uninstalling template.
    Installing template.
    >>> cat('bar')
    FOO !

Just like context definition, it also works with indirect values::

    >>> write('buildout.cfg', '''
    ... [buildout]
    ... parts = template
    ...
    ... [template-library]
    ... path = library.in
    ...
    ... [template]
    ... recipe = slapos.recipe.template:jinja2
    ... template = template.in
    ... rendered = bar
    ... import-list = file library template-library:path
    ... ''')
    >>> run_buildout()
    Uninstalling template.
    Installing template.
    >>> cat('bar')
    FOO !

This also works to allow importing from identically-named files in different
directories::

    >>> write('template.in', '''
    ... {%- import "dir_a/1.in" as a1 -%}
    ... {%- import "dir_a/2.in" as a2 -%}
    ... {%- import "dir_b/1.in" as b1 -%}
    ... {%- import "dir_b/c/1.in" as bc1 -%}
    ... {{ a1.foo() }}
    ... {{ a2.foo() }}
    ... {{ b1.foo() }}
    ... {{ bc1.foo() }}
    ... ''')
    >>> mkdir('a')
    >>> mkdir('b')
    >>> mkdir(join('b', 'c'))
    >>> write(join('a', '1.in'), '{% macro foo() %}a1foo{% endmacro %}')
    >>> write(join('a', '2.in'), '{% macro foo() %}a2foo{% endmacro %}')
    >>> write(join('b', '1.in'), '{% macro foo() %}b1foo{% endmacro %}')
    >>> write(join('b', 'c', '1.in'), '{% macro foo() %}bc1foo{% endmacro %}')

All templates can be accessed inside both folders::

    >>> write('buildout.cfg', '''
    ... [buildout]
    ... parts = template
    ...
    ... [template-library]
    ... path = library.in
    ...
    ... [template]
    ... recipe = slapos.recipe.template:jinja2
    ... template = template.in
    ... rendered = bar
    ... import-list =
    ...     rawfolder dir_a a
    ...     rawfolder dir_b b
    ... ''')
    >>> run_buildout()
    Uninstalling template.
    Installing template.
    >>> cat('bar')
    a1foo
    a2foo
    b1foo
    bc1foo

It is possible to override default path delimiter (without any effect on final
path)::

    >>> write('template.in', r'''
    ... {%- import "dir_a\\1.in" as a1 -%}
    ... {%- import "dir_a\\2.in" as a2 -%}
    ... {%- import "dir_b\\1.in" as b1 -%}
    ... {%- import "dir_b\\c\\1.in" as bc1 -%}
    ... {{ a1.foo() }}
    ... {{ a2.foo() }}
    ... {{ b1.foo() }}
    ... {{ bc1.foo() }}
    ... ''')
    >>> write('buildout.cfg', r'''
    ... [buildout]
    ... parts = template
    ...
    ... [template-library]
    ... path = library.in
    ...
    ... [template]
    ... recipe = slapos.recipe.template:jinja2
    ... template = template.in
    ... rendered = bar
    ... import-delimiter = \
    ... import-list =
    ...     rawfolder dir_a a
    ...     rawfolder dir_b b
    ... ''')
    >>> run_buildout()
    Uninstalling template.
    Installing template.
    >>> cat('bar')
    a1foo
    a2foo
    b1foo
    bc1foo

Section dependency
------------------

You can use other part of buildout in the template. This way this parts
will be installed as dependency::

    >>> write('buildout.cfg', '''
    ... [buildout]
    ... parts = template
    ...
    ... [template]
    ... recipe = slapos.recipe.template:jinja2
    ... template = inline:{{bar}}
    ... rendered = foo
    ... context = key bar dependency:foobar
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

    >>> write('buildout.cfg',
    ... '''
    ... [buildout]
    ... develop = .
    ... parts = template
    ...
    ... [template]
    ... recipe = slapos.recipe.template:jinja2
    ... template = inline:
    ...   {{bar}}
    ... rendered = foo
    ... context = key bar sample:data
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
    >>> cat('foo')
    foobar

Avoiding file re-creation
~~~~~~~~~~~~~~~~~~~~~~~~~

Normally, each time the section is installed/updated the file gets
re-generated. This may be undesirable in some cases.

``once`` allows specifying a marker file, which when present prevents template
rendering.

    >>> import os
    >>> write('buildout.cfg',
    ... '''
    ... [buildout]
    ... parts = template
    ...
    ... [template]
    ... recipe = slapos.recipe.template:jinja2
    ... template = inline:dummy
    ... rendered = foo_once
    ... once = foo_flag
    ... ''')
    >>> run_buildout() # doctest: +ELLIPSIS
    Uninstalling template.
    Uninstalling sample.
    Getting distribution for 'samplerecipe'.
    Got samplerecipe 0.0.0.
    Installing template.
    The template install returned None.  A path or iterable os paths should be returned.
    warning: install_lib: '...' does not exist -- no Python modules to install
    <BLANKLINE>
    zip_safe flag not set; analyzing archive contents...

Template was rendered::

    >>> cat('foo_once')
    dummy

And canary exists::

    >>> os.path.exists('foo_flag')
    True

Remove rendered file and re-render::

    >>> import os
    >>> os.unlink('foo_once')
    >>> with open('buildout.cfg', 'a') as f:
    ...     f.writelines(['extra = useless'])
    >>> run_buildout()
    Uninstalling template.
    Installing template.
    The template install returned None.  A path or iterable os paths should be returned.
    Unused options for template: 'extra'.

Template was not rendered::

   >>> os.path.exists('foo_once')
   False

Removing the canary allows template to be re-rendered::

    >>> os.unlink('foo_flag')
    >>> with open('buildout.cfg', 'a') as f:
    ...     f.writelines(['moreextra = still useless'])
    >>> run_buildout()
    Uninstalling template.
    Installing template.
    The template install returned None.  A path or iterable os paths should be returned.
    Unused options for template: 'extra'.
    >>> cat('foo_once')
    dummy

It's also possible to use the same file for ``rendered`` and ``once``::

    >>> write('buildout.cfg',
    ... '''
    ... [buildout]
    ... parts = template
    ...
    ... [template]
    ... recipe = slapos.recipe.template:jinja2
    ... template = inline:initial content
    ... rendered = rendered
    ... once = ${:rendered}
    ... ''')
    >>> run_buildout() # doctest: +ELLIPSIS
    Uninstalling template.
    Installing template.
    The template install returned None.  A path or iterable os paths should be returned.

Template was rendered::

    >>> cat('rendered')
    initial content

When buildout options are modified, the template will not be rendered again::

    >>> with open('buildout.cfg', 'a') as f:
    ...     f.writelines(['template = inline:something different'])

    >>> run_buildout()
    Uninstalling template.
    Installing template.
    The template install returned None.  A path or iterable os paths should be returned.

Even though we used a different template, the file still contain the first template::

    >>> cat('rendered')
    initial content
