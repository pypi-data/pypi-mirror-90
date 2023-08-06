##############################################################################
#
# Copyright (c) 2009 Projekt01 GmbH and Contributors.
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
$Id:$
"""
__docformat__ = "reStructuredText"

import xmlrpclib

import transaction
import zope.interface
import zope.component
import zope.event
import zope.lifecycleevent
from zope.schema.fieldproperty import FieldProperty
from zope.container import btree

from z3c.configurator import configurator

import mypypi.api
import mypypi.exceptions
import mypypi.release
from mypypi import interfaces
from mypypi.i18n import MessageFactory as _


class PackageMixin(btree.BTreeContainer):
    """IPackage mixin."""

    published = FieldProperty(interfaces.IPackage['published'])

    def __setitem__(self, __name__, release):
        """Disabeld, use add method instead."""
        if not interfaces.IRelease.providedBy(release):
            raise ValueError('Not a release given.')
        super(PackageMixin, self).__setitem__(__name__, release)

    @property
    def isPublished(self):
        if not self.published:
            return False
        published = False
        for release in self.values():
            if release.isPublished:
                return True
        return False

    @property
    def latest(self):
        version = ''
        current = None
        for release in self.values():
            # version is a number with letters in unicode which means
            # '0.5.0a' is later then '0.5.0'. But anyway you never should
            # use letters in release numbers. probably we should be smart and
            # support such addon letters which mark earlier releases.
            if release.version > version:
                version = release.version
                current = release
        return current

    def __repr__(self):
        return "<%s %r>" %(self.__class__.__name__, self.__name__)


class LocalPackage(PackageMixin):
    """Package located only at this server."""

    zope.interface.implements(interfaces.ILocalPackage)


class MirrorPackage(PackageMixin):
    """Package mirrored from another package index."""

    zope.interface.implements(interfaces.IMirrorPackage)

    pypiURL = FieldProperty(interfaces.IMirrorPackage['pypiURL'])

    def __init__(self, pypiURL):
        super(MirrorPackage, self).__init__()
        self.pypiURL = pypiURL

    @property
    def url(self):
        return '%s/%s/json' % (self.pypiURL, self.__name__)

    def update(self):
        try:
            client = mypypi.api.getAPIClient()
            data = client.getPackageData(url=self.url)
        except mypypi.exceptions.PackageError, e:
            msg = _('Error: Can not get package releases for package: '
                    '$name', mapping={'name': self.__name__})
            mypypi.api.logMirrorError(msg, self.url)
            raise mypypi.exceptions.MissingReleases(self.__name__)
        for name, rd in data['releases'].items():
            # create release
            release = self.get(name)
            if release is not None:
                release.update(rd, client)
                continue

            added = True
            obj = mypypi.release.MirrorRelease()
            zope.event.notify(zope.lifecycleevent.ObjectCreatedEvent(obj))
            # add release
            self[name] = obj
            transaction.commit()
            obj.update(rd, client)

        # marke as modified which will force to save a new modified date
        zope.event.notify(zope.lifecycleevent.ObjectModifiedEvent(self))


class MirrorPackageConfigurator(configurator.ConfigurationPluginBase):
    """Configure the IMirrorPackage."""

    zope.component.adapts(interfaces.IMirrorPackage)

    def __call__(self, data):
        self.context.update()
