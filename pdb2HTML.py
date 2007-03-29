#!/usr/bin/env python

import os
from gimpfu import *

type_name = {
	0:	"INT32",
	1:	"INT16",
	2:	"INT8",
	3:	"FLOAT",
	4:	"STRING",
	5:	"INT32ARRAY",
	6:	"INT16ARRAY",
	7:	"INT8ARRAY",
	8:	"FLOATARRAY",
	9:	"STRINGARRAY",
	10:	"COLOR",
	12:	"DISPLAY",
	13:	"IMAGE",
	14:	"LAYER",
	15:	"CHANNEL",
	16:	"DRAWABLE",
	17:	"SELECTION",
	20:	"PARASITE",
}

def HTMLesc(string):
	string = string.replace('&', '&amp;')
	string = string.replace('<', '&lt;')
	string = string.replace('>', '&gt;')
	return string


def proc_desc(procname, anchorname):
	proc = gimp.pdb[procname]
	text = []
	text.append('<h2><a name="%s"></a>%s</h2>' % (anchorname, procname))
	if proc.proc_blurb:
		text.append('<p class="b">%s</p>' % HTMLesc(proc.proc_blurb))
	if proc.proc_blurb.lower() != proc.proc_help.lower():
		text.append('<p class="h">%s</p>' % HTMLesc(proc.proc_help))

	if proc.nparams:
		if proc.nparams > 1:
			text.append('<h3>Parameters</h3>')
		else:
			text.append('<h3>Parameter</h3>')
			
		text.append('<table class="p">')
		for type, name, desc in proc.params:
			type = type_name.get(type, '<font color="red">%s</font>' % str(type))
			text.append('<tr><td>%s</td><td><i>%s</i></td><td>%s</td></tr>' % (name, type, desc))
		text.append('</table>')
	else:
		pass
		#text.append('<h3>Takes no parameters</h3>')
	
	if proc.nreturn_vals:
		if proc.nreturn_vals > 1:
			text.append('<h3>Return values</h3>')
		else:
			text.append('<h3>Return value</h3>')
		text.append('<table class="r">')
		for type, name, desc in proc.return_vals:
			type = type_name.get(type, '<font color="red">%s</font>' % str(type))
			text.append('<tr><td>%s</td><td><i>%s</i></td><td>%s</td></tr>' % (name, type, HTMLesc(desc)))
		text.append('</table>')
	
	if proc.proc_author or proc.proc_copyright or proc.proc_date:
		text.append('<h3>Additional information</h3>')
		text.append('<table class="e">')
		if proc.proc_author:
			text.append('<tr><td><b>Author:</b></td><td>%s</td>' % HTMLesc(proc.proc_author))
		if proc.proc_date:
			text.append('<tr><td><b>Date:</b></td><td>%s</td>' % HTMLesc(proc.proc_date))
		if proc.proc_copyright:
			text.append('<tr><td><b>Copyright:</b></td><td>%s</td>' % HTMLesc(proc.proc_copyright))
		text.append('</table>')
	
	return text


def convert(procnamelist, desc, title):
	cssname  = "gimpfun.css"

	text = []
	text.append("<html>")
	text.append("<meta>")
	text.append("<title>%s</title>" % title)
	text.append('<link rel="stylesheet" href="%s" type="text/css">' % cssname)
	text.append("</meta>")
	text.append("<body>")
	text.append("<h1>%s</h1>" % title)
	text.append("<ul>")
	
	for name in sorted(procnamelist):
		blurb = pdb[name].proc_blurb.strip()
		if blurb and blurb[-1] == ".":
			blurb = blurb[:-1]

		if blurb:
			text.append('<li><a href="#%s">%s</a> - %s</li>' % (name, name, HTMLesc(blurb)))
		else:
			text.append('<li><a href="#%s">%s</a></li>' % (name, name))
	text.append("</ul>")

	for procname in sorted(procnamelist):
		text.extend( desc[procname] )
	
	text.append("</body>")
	text.append("</html>")

	return text


def python_pdb2HTML(basedir):
	prefixes = "extension file gimp plug_in script_fu python_fu".split()

	if not os.path.exists(basedir):
		os.makedirs(basedir)
	
	gimp.progress_init("Gathering info...")
	procnamelist = gimp.pdb.query()
	progstep = 1.0/(len(procnamelist)-1)
	desc = {}
	for i, procname in enumerate(procnamelist):
		desc[procname] = proc_desc(procname, procname)
		gimp.progress_update(i*progstep)

	gimp.progress_init("Saving...")
	progstep = 1.0/(len(prefixes)+1)
	progress = 0.0

	f = open(os.path.join(basedir, "gimp-all.html"), 'w')
	for line in convert(procnamelist, desc, "All GIMP functions"):
		f.write(line + "\n")
	f.close()

	progress += progstep
	gimp.progress_update(progress)
	
	for prefix in prefixes:
		f = open(os.path.join(basedir, "gimp-%s.html" % prefix), "w")
		list = [name for name in procnamelist if name.startswith(prefix)]
		for line in convert(list, desc, "GIMP functions - %s" % prefix):
			f.write(line + "\n")
		f.close()
		progress += progstep
		gimp.progress_update(progress)


register(
        "python_fu_savedoc",
        "Save in HTML format descriptions of functions available for programmers",
        "Static version of PDB browser",
        "Wojciech Mula <wojciech_mula@poczta.onet.pl>",
        "Wojciech Mula",
        "2007",
        "<Toolbox>/Xtns/Python-Fu/_Save docs in HTML format",
        "INDEXED*, RGB*, GRAY*",
        [
			(PF_STRING, "basedir", "The path to export the HTML to", os.getcwd()),
		],
        [],
        python_pdb2HTML)

main()

# vim: ts=4 sw=4 nowrap noexpandtab
