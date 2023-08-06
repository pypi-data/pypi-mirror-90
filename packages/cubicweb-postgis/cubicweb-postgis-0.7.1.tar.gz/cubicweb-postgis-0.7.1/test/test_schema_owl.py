# copyright 2020 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact https://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <https://www.gnu.org/licenses/>.


from xml.dom.minidom import parseString as parseXmlString

from cubicweb.devtools.testlib import CubicWebTC


class OWLViewTC(CubicWebTC):

    def test_owl_schema_valid_xml(self):
        with self.new_access('admin').web_request() as req:
            pageinfo = self.view('owl', req=req)
            self.assertIn('owl', pageinfo.source.decode('utf-8'))
            self.assertTrue(parseXmlString(pageinfo.source))


if __name__ == "__main__":
    import unittest
    unittest.main()
