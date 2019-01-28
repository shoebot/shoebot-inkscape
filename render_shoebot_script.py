'''
Copyright (C) 2008 ricardo lafuente

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
'''

import sys, os
sys.path.append('/usr/share/inkscape/extensions')

import inkex
import shoebot

TEMPFILE = "/home/rlafuente/shoebot_temp.svg"

def parse_svg_file(file):
        """Parse document in specified file

        taken from the SVG and media zip output plugin"""
        stream = open(file,'r')
        doc = inkex.etree.parse(stream)
        stream.close()
        return doc

class InsertShoebotOutput(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("-p", "--path",
                        action="store", type="string",
                        dest="path", default='',
                        help="Botscript path")

    def effect(self):

        ## x, y = self.view_center

        # fire the shoebot console runner and output to a tempfile
        script = self.options.path
        command = 'sbot %s -o %s' % (script, TEMPFILE)
        c,out,err = os.popen3(command,'r')

        if out.read():
            sys.stdout.write(out.read())

        # show error dialog in case shoebot complained
        if err.read():
            sys.stderr.write("Shoebot error: " + err.read())

        # read file contents
        tree = parse_svg_file(TEMPFILE)
        # we don't need the file anymore now
        os.remove(TEMPFILE)

        # get the root node of the tree
        svg_data = tree.getroot()

        # create a new layer in the open document
        svg = self.document.getroot()
        layer = inkex.etree.SubElement(svg, 'g')
        layer.set(inkex.addNS('label', 'inkscape'), 'Shoebot output')
        layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')

        # get the tree data into the new layer
        # we need to check nodes below the root one
        for node in svg_data:
            layer.append(node)

e = InsertShoebotOutput()
e.affect()

