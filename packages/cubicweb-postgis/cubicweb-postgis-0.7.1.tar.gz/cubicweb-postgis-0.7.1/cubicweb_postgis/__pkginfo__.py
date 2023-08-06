# pylint: disable=W0622
"""cubicweb-postgis application packaging information"""

modname = 'postgis'
distname = 'cubicweb-%s' % modname

numversion = (0, 7, 1)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'Test for postgis'
web = 'https://www.cubicweb.org/project/%s' % distname

__depends__ = {
    'cubicweb': '>= 3.26.19',
}
__recommends__ = {}

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Programming Language :: JavaScript',
    'Topic :: Scientific/Engineering :: GIS',
    'Topic :: Database',
]
