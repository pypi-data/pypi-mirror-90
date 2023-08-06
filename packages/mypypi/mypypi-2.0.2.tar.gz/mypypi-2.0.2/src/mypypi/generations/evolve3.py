##############################################################################
#
# Copyright (c) 2015 Projekt01 GmbH and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
$Id: evolve3.py 5063 2021-01-05 02:44:16Z roger.ineichen $
"""
__docformat__ = "reStructuredText"

import os
import os.path
import time
import shutil

import logging

import zope.event
import zope.lifecycleevent
from zope.component import hooks
from zope.intid.interfaces import IIntIds
from zope.app.generations.utility import getRootFolder

from z3c.indexer.interfaces import IIndex

import p01.fsfile.interfaces

import mypypi.storage
import mypypi.release
import mypypi.public
import mypypi.project


LOGGER = logging.getLogger('generation3')


def doRemoveIndexes(site, sm):
    """Remove all indexes and catalogs"""
    del sm['default']['package.packageText']

    del sm['default']['package.isPublished']

    del sm['default']['package.releaseText']

    del sm['default']['package.releaseClassifiers']

    del sm['default']['release.fullText']

    del sm['default']['user.fullText']

    del sm['default']['historyEntry.fullText']

    del sm['default']['errorEntry.fullText']

    del sm['default']['IntIds' ]


def evolve(context):
    """Evolve the ZODB.

    - remove all indexes and intid util

    """
    site = getRootFolder(context)

    LOGGER.warn("Start generation")

    # set the evolving site as the site
    originalSite = hooks.getSite()
    hooks.setSite(site)
    sm = site.getSiteManager()

    # remove indexes
    doRemoveIndexes(site, sm)

    # set original site back
    hooks.setSite(originalSite)
