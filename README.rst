========================================================================
                           GIMP plugins
========================================================================

Last update: 29.03.2007


Plugins sources have to be placed in ``{home}/.gimp-{version}/plug-ins``,
and must have executable attribute.


Clear grayscale scans
------------------------------------------------------------------------

This plugin clears background of b/w scanned images.  Image, i.e
letters/drawing have to be clear, and background should have low
amount of dust, like on picture below.  In other cases result won't
be good

* `clear_gscans.py <clear_gscans.py>`_

Plugin is available from ``Filters`` menu.

Before:
	.. image:: cgs-before.png

After:
	.. image:: cgs-after.png



Save in HTML format descriptions of functions available for programmers
------------------------------------------------------------------------

Static version of PDB browser available in GIMP.
Plugin is available from ``Tools/Python-fu`` menu.

* `pdb2HTML.py <pdb2HTML.py>`_


License
------------------------------------------------------------------------

Plugins are licensed under BSD-license.
