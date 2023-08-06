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
$Id: evolve2.py 5061 2021-01-04 16:49:58Z roger.ineichen $
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


LOGGER = logging.getLogger('generation2')


def doRemoveIndexes(site, sm):
    """Remove all indexes and catalogs"""
    idx = sm['default']['package.packageText']
    sm.unregisterUtility(idx, IIndex, name='package.packageText')

    idx = sm['default']['package.isPublished']
    sm.unregisterUtility(idx, IIndex, name='package.isPublished')

    idx = sm['default']['package.releaseText']
    sm.unregisterUtility(idx, IIndex, name='package.releaseText')

    idx = sm['default']['package.releaseClassifiers']
    sm.unregisterUtility(idx, IIndex, name='package.releaseClassifiers')

    idx = sm['default']['release.fullText']
    sm.unregisterUtility(idx, IIndex, name='release.fullText')

    idx = sm['default']['user.fullText']
    sm.unregisterUtility(idx, IIndex, name='user.fullText')

    idx = sm['default']['historyEntry.fullText']
    sm.unregisterUtility(idx, IIndex, name='historyEntry.fullText')

    idx = sm['default']['errorEntry.fullText']
    sm.unregisterUtility(idx, IIndex, name='errorEntry.fullText')

    util = sm['default']['IntIds' ]
    for key in list(util.ids.keys()):
        try:
            del util.ids[key]
        except Exception as e:
            pass
    for key in list(util.refs.keys()):
        try:
            del util.refs[key]
        except Exception as e:
            pass
    sm.unregisterUtility(util, IIntIds)


def doRemoveRemoteProcessor(site):
    """Remove remote processor and jobs"""

    # cleanup processor
    for key in list(site._processor.keys()):
        try:
            del site._processor[key]
        except Exception as e:
            pass

    for key in list(site._jobs.keys()):
        try:
            del site._jobs[key]
        except Exception as e:
            pass

    # cleanup scheduler
    for key in list(site._scheduler._items.keys()):
        try:
            del site._scheduler._items[key]
        except Exception as e:
            pass

    # remove references
    site._scheduler._pending = None
    site._scheduler.__parent__ = None
    site._scheduler = None

    site._jobs = None
    site._processor = None
    site._queue = None


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

    # remove remote processor, schendluer and jobs
    doRemoveRemoteProcessor(site)

    # set original site back
    hooks.setSite(originalSite)
