Sample Galaxy tools that use this package
-----------------------------------------

These tools are meant to be installed locally (not from a toolshed).

We provide two variants - one that imports and uses the module from a Python wrapper,
and another that call a script directly from XML tool config. They are located
under tools subdirectory.

You will also need to add vigor.tgz datatype to the Galaxy's datatypes_conf.xml (see
the definition sample file in this directory).

You also need to edit universe_wsgi.ini and switch off HTML sanitization:
sanitize_all_html = False

