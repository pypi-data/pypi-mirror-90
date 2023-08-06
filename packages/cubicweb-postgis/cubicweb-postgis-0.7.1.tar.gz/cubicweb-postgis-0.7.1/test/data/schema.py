# -*- coding: utf-8 -*-
# copyright 2015 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
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
# with this program. If not, see <http://www.gnu.org/licenses/>.

from yams.buildobjs import EntityType, String

from cubicweb_postgis.schema import Geometry, Geography


class City(EntityType):
    name = String(required=True, maxsize=100)
    center_4326 = Geometry(srid=4326, geom_type='POINT')
    center_nosrid = Geometry(srid=-1, geom_type='POINT')
    limits = Geography(geom_type='POLYGON')
