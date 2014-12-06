pywebfunk
=========

Scaleable Object-Oriented Python Web Design Framework

The purpose of this project is to provide a unified place (a script) to generate
cross-site UI components in a programmatic way.  I want to be able to use this
to quickly modify site design and also be able to manually or automatically use
this to adjust UI components for A/B testing.

Currently the \_\_main\_\_ function in the pywebfunk.py module shows how to use
the library.  Mainly, you have a document that Components can be added to.

A Component overrides its \_\_str\_\_ method appropriately.  Any Component is
initialized with any necessary tags as keyword args.

Divs are Containers and Components.  Divs will render any contained elements and
will apply any necessary tags on themselves.

Css hierarchy
=============
Currently you create css using the css constructor like so:
css(".div", background\_color="yellow", ...)

.div is the selector, and any keyword properties with a "-" dash are written
with an underscore.

Css gets added to style sheets, but I would like to enable a way to have the Css
self-organize itself.  Various rules could be applied to elements and element
and class-wise css classes get created dynamically.  (Although this is low on
the priorities list.)


Todo
=====
* I would like to add easy table support, and then add support for a js library
like gridster with a similar or identical interface.
* Investigate the applicator interface and see if it's worth the time.
* Work on template support / template creation.
