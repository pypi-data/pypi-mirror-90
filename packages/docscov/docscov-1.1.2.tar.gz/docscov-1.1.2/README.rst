DocsCov
=======

DocsCov is a Sphinx extension that allows you to show a badge showing
documentation coverage for C++ (or any other Doxygen supported) code.


Getting Started
---------------

First, install it by (requires python 3.6+):

    pip install docscov

You need to use Doxygen to generate XML data about the source files. To do that,
add the following to your Doxygen configuration: (not needed if you're using
tools like Breathe or Exhale, you should have this already)

    GENERATE_XML = YES

This will generate XML data about source files. Now just add ``docscov`` to your
Sphinx extensions and add the following to your ``conf.py``:

.. code-block:: python

    docscov_config = {
        "xml_dir": "<path to generated XML by Doxygen>"
    }

It'll places a JSON file inside built documentations, which can be used with
`Shields <https://shields.io>`_ to make a dynamic badge, updated each time
documentations are built.


Getting the badge
+++++++++++++++++

To get the badge do the following:

1. Get the URL to your generated documentations (with ``http://`` or
   ``https://``)
2. Replace the ``:`` with ``%3A`` in the URL
3. Replace all slashes (``/``) in the text you got by completing step 2
4. Replace ``<url>`` in the following text with the text you got by completing
   step 3, and the text you'll get is the URL to your badge that can be placed in
   your README:

    https://img.shields.io/endpoint?url=<url>%2F_static%2Fdocscov.json

Example: `<https://pypp.readthedocs.io/en/latest>`_ will be converted to this
after following above:
`<https://img.shields.io/endpoint?url=https%3A%2F%2Fpypp.readthedocs.io%2Fen%2Flatest%2F_static%2Fdocscov.json>`_


Configurable options
--------------------

You can configure DocsCov with the following options:

``xml_dir``:

    **Value type:** ``str``

    **Description:** Path to Doxygen XML output

``root_dir``:

    **Value type:** ``str``

    **Description:** Path to process relative directories.

    **Notes:** *Optional*.

    **Default:** ``'.'``

``badge_label``:

    **Value type:** ``str``

    **Description:** The label of badge.

    **Notes:** *Optional*.

    **Default:** ``'docscov'``

``scope``:

    **Value type:** ``list``

    **Description:** Coverage scope. Possible values of elements:

    * ``public``: Include public members of classes
    * ``protected``: Include protected members of classes
    * ``private``: Include private members of classes
    * ``all``: All of above

    **Notes:** *Optional*.

    **Default:** ``['all']``

``kind``:

    **Value type:** ``list``

    **Description:** Kind of definitions to include in coverage. Possible values
    of elements:
    
    * ``class``
    * ``define``
    * ``enum``
    * ``enumvalue``
    * ``file``
    * ``friend``
    * ``function``
    * ``namespace``
    * ``page``
    * ``signal``
    * ``slot``
    * ``struct``
    * ``typedef``
    * ``union``
    * ``variable``
    * ``all``: All of above

    **Notes:** *Optional*.

    **Default:** ``['all']``
