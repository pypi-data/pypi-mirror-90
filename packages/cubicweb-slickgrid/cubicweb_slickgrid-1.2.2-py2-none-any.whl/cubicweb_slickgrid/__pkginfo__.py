# pylint: disable=W0622
#
# copyright 2003-2021 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
#
# Developped by Logilab S.A. (Paris, FRANCE) https://www.logilab.fr
#
"""cubicweb-slickgrid application packaging information"""

from os.path import dirname, join


modname = 'slickgrid'
distname = 'cubicweb-%s' % modname

# Version lives in a dedicated file to ease automation.
with open(join(dirname(__file__), 'VERSION')) as f:
    version = f.readline().strip()
numversion = tuple(int(num) for num in version.split('.')[:3])

license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'Table view rendered using the SlickGrid_ JavaScript library.'
web = 'https://www.cubicweb.org/project/%s' % distname

__depends__ = {
    'cubicweb': '>= 3.26.19',
    'six': '>= 1.12.0',
}
__recommends__ = {}

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Programming Language :: JavaScript',
]
