Example of Galaxy toolshed package.
The xml and python files here are slightly out of date with regard to the current
method signatures of the VICVB package. Because currently there is no clean way to
install a toolshed repo programmatically (without clicking through Galaxy UI),
we are not releasing a toolshed tool anyway.
This registers a display application and a converter, so that the display 
application can be invoked after an implicit conversion.
The display application currently does not work for our application
because JBrowse needs to access a directory tree under $input.extra_files_path,
and there seems to be no way to expose that one under the display application
"route" within Paste Web server in Galaxy (see lib/galaxy/webapps/galaxy/buildapp.py 
for "display" controller, which is an action taken when the user clicks Eye
icon - the route is defined for that one and we have access - see also
http://lists.bx.psu.edu/pipermail/galaxy-dev/2011-March/004701.html).
Getting to the files in a composite datatype should also work like
<a href="display_child?parent_id=2&designation=some_file_name">Some Text</a>
but it does not (parent_id must be the dataset ID, not history ID).
Code is in lib/galaxy/webapps/galaxy/controllers/root.py
Maybe the child has to be registered somehow.

Viewing the dataset will still work through the "display" (Eye icon) JS hack,
assuming sanitize_all_html=False in universe_wsgi.ini.
A sample universe_wsgi.ini is included here.
