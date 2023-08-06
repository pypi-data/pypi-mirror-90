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

import copy
import time
import StringIO
import cStringIO
import os
import re
import sys
import types
import urllib
import urllib2
import urlparse
import httplib
import zipfile
import HTMLParser
import logging
# import xmlrpclib
from glob import fnmatch
from pkg_resources import parse_version
from docutils.core import publish_parts
try:
   from hashlib import md5
except ImportError:
   from md5 import md5

import requests

from BeautifulSoup import BeautifulSoup

from zope.component import hooks
from zope.security import checkPermission

import mypypi.exceptions
from mypypi import interfaces
from mypypi import logger
from mypypi import versionpredicate

DEFAULT_PYPI_URL = 'https://pypi.org/pypi'

LOGGER = logging.getLogger('mypypi')

##############################################################################
#
# logging

def logLocalHistory(message):
    log = logger.getLocalLogger()
    log.logHistory(message)

def logLocalError(message):
    log = logger.getLocalLogger()
    log.logError(message)

def logMirrorHistory(message, path=None):
    log = logger.getMirrorLogger()
    log.logHistory(message, path)

def logMirrorError(message, path=None):
    log = logger.getMirrorLogger()
    log.logError(message, path)


##############################################################################
#
# simple page rendering

PAGE = """<html>
<head><title>%s</title>
</head>
<body>
<h1>%s</h1>
%s
</body>
</html>
"""

def renderOneLineLink(url, content):
    return '<a href="%s">%s</a>' % (url, content)

def renderPage(page):
    return PAGE % (page.title, page.title, page.body)


def markItemsAsPublished(item, state=True):
    item.published = state
    if interfaces.IPackage.providedBy(item) or \
        interfaces.ILocalRelease.providedBy(item) or \
        interfaces.IMirrorRelease.providedBy(item):
        for child in item.values():
            markItemsAsPublished(child, state)


def checkViewPermission(obj):
    return checkPermission('mypypi.View', obj)


def checkManagePackagesPermission(obj):
    return checkPermission('mypypi.ManagePackages', obj)


def checkViewable(obj=None):
    if obj is None:
        return False
    # check first permision then publish stati, otherwise we will
    #  run into Unauthorized if we access isPublished first
    return checkPermission('mypypi.View', obj) and  obj.isPublished


##############################################################################
#
# proxy

def getProxies():
    """Returns the proxy dict {protocol:url} from IPYPISite"""
    site = hooks.getSite()
    if interfaces.IPYPISite.providedBy(site):
        proxies = site.proxies or {}
    else:
        proxies = {}
    res = {}
    for proto, url in proxies.items():
        res[str(proto)] = str(url)
    return res


##############################################################################
#
# new api client

_urlopen = urllib2.urlopen

class APIClient(object):
    """API client"""

    # exposed for testing purposes.
    _sessionFactory = requests.Session

    def __init__(self, timeout=10.0, max_retries=2, headers=None):
        """Setup requests connection"""
        self.proxies = getProxies()
        self.timeout = timeout
        self.max_retries = max_retries
        # requests session
        self.session = self._sessionFactory()
        if headers is not None:
            headers = copy.copy(headers)
            self.session.headers.update(headers)
        for adapter in self.session.adapters.values():
            adapter.max_retries = self.max_retries

    @property
    def isTesting(self):
        # patched or not?
        return self._sessionFactory != requests.Session

    def doLogInfo(self, msg):
        LOGGER.info(msg)

    def doLogError(self, msg):
        LOGGER.error(msg)

    def doLogException(self, e):
        LOGGER.exception(e)

    # http request
    def doRequest(self, method, url, headers=None, params=None, data=None,
        jData=None, verify=False):
        """This method allows to use a testing hook"""
        if url is None:
            msg = "No url given %s" % url
            self.doLogError(msg)
            raise mypypi.exceptions.PackageError
        # log request
        self.doLogInfo("Request: %s" % url)
        resp = self.session.request(method, url, headers=headers,
            params=params, data=data, json=jData, proxies=self.proxies,
            verify=verify)
        #self.doLogInfo("Response: %s, Content: %r" % (url, resp.content))
        return resp

    def getPackageData(self, url):
        self.doLogInfo("Get package data from: %s" % url)
        resp = self.doRequest('GET', url)
        if resp.status_code == 200:
            return resp.json()
        else:
            self.doLogError(
                "RESPONSE: %d \nResponse headers: %s \nMessage from solique: %s" % (
                resp.status_code, resp.headers, resp.content))
            raise mypypi.exceptions.PackageError

    def getReleaseData(self, url):
        self.doLogInfo("Get release data from: %s" % url)
        resp = self.doRequest('GET', url)
        if resp.status_code == 200:
            return resp.json()
        else:
            self.doLogError(
                "RESPONSE: %d \nResponse headers: %s \nMessage from solique: %s" % (
                resp.status_code, resp.headers, resp.content))
            raise mypypi.exceptions.PackageError

    def getReleaseFile(self, url, filename, md5Digest=None):
        """Fetches a release file and checks for the md5Digest if given."""
        self.doLogInfo("Get release file: %s from: %s" % (filename, url))
        data = None
        try:
            # we use a new session with self.session because the
            #
            # resp = self.session.request('GET', url, verify=False)
            resp = self.doRequest('GET', url)
            if resp.ok:
                data = resp.content
                if md5Digest and not self.isTesting:
                    # check for md5 checksum if we are not in test mode using
                    # a patched requests library whic is not providing the
                    # correcet md5 checksum
                    data_md5 = md5(data).hexdigest()
                    if md5Digest != data_md5:
                        raise mypypi.exceptions.PackageError(
                            "MD5 sum does not match: %s / %s for release file %s" % (
                                md5Digest, data_md5, url))
        except urllib2.URLError as e:
            raise mypypi.exceptions.PackageError("URL Error: %s " % url)
        except Exception as e:
            self.doLogException(e)
            raise mypypi.exceptions.PackageError(
                "Couldn't download (HTTP Error): %s" % url)
        return data


    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__)


def getAPIClient(url=None):
    return APIClient()


##############################################################################
#
# apply release data

def makeList(value):
    # convert to unicode lists
    return [unicode(v) for v in value]

# format is: {incoming_field: (camelcasedField, valueConverter)}
RELEASE_DATA = {
    # '_pypi_hidden': ('pypiHidden', int),
    # '_pypi_ordering': ('pypiOrdering', int),
    'author': ('author', unicode),
    'author_email': ('authorEmail', unicode),
    'cheesecake_code_kwalitee_id': ('cheesecakeCodeKwaliteeId', int),
    'cheesecake_documentation_id': ('cheesecakeDocumentationId', int),
    'cheesecake_installability_id': ('cheesecakeInstallabilityId', int),
    'classifiers': ('classifiers', makeList),
    'description': ('description', unicode),
    'download_url': ('downloadURL', unicode),
    'home_page': ('homePage', unicode),
    'keywords': ('keywords', unicode),
    'license': ('license', unicode),
    'maintainer': ('maintainer', unicode),
    'maintainer_email': ('maintainerEmail', unicode),
    'md5_digest': ('md5Digest', str),
    'name': ('name', unicode),
    'obsoletes': ('obsoletes', makeList),
    'platform': ('platform', unicode),
    'protocol_version': ('protocolVersion', unicode),
    'provides': ('provides', makeList),
    'requires': ('requires', makeList),
    'stable_version': ('stableVersion', unicode),
    'summary': ('summary', unicode),
}

RELEASE_FILE_DATA = {
    'comment_text': ('commentText', unicode),
    'downloads': ('downloads', int),
    # distutils uses filetype and pypi uses packagetype, we use packageType
    'filetype': ('packageType', unicode),
    'has_sig': ('hasSig', bool),
    'md5_digest': ('md5Digest', str),
    # distutils uses filetype and pypi uses packagetype, we use packageType
    'packagetype': ('packageType', unicode),
    'python_version': ('pythonVersion', unicode),
    'size': ('size', int),
    'url': ('url', str),
}

def applyData(context, data, lookupTable):
    for key, value in data.items():
        # oh my, we only use camel case
        # release data
        newData = lookupTable.get(key)
        if newData is None:
            # skip unknown attributes
            continue

        key = newData[0] # camel case key
        converter = newData[1] # converter

        # convert value
        if converter is not None and value:
            try:
                value = converter(value)
            except ValueError, e:
                raise ValueError("Can't convert value %s to %s for %s" % (
                    value, converter, key))
        # apply value
        if value:
            setattr(context, key, value)


def applyReleaseData(context, data):
    applyData(context, data, RELEASE_DATA)

def applyReleaseFileData(context, data):
    applyData(context, data, RELEASE_FILE_DATA)


################################################################################
#
# setuptools

# distutil upload helper
allowedFileNames = re.compile(r'.+?\.(exe|tar\.gz|bz2|egg|rpm|deb|zip|tgz)$',
    re.I)

def verifyMetaData(data, verifyClassifiers=True):
    """ Validate the contents of the metadata.
    """
    if not data.get('name', ''):
        raise ValueError, 'Missing required field "name"'
    if not data.get('version', ''):
        raise ValueError, 'Missing required field "version"'
    if data.has_key('metadata_version'):
        del data['metadata_version']

    # make sure relationships are lists
    for name in ('requires', 'provides', 'obsoletes'):
        if data.has_key(name) and not isinstance(data[name], list):
            data[name] = [data[name]]

    # make sure classifiers is a list
    if data.has_key('classifiers'):
        classifiers = data['classifiers']
        if not isinstance(classifiers, list):
            classifiers = [classifiers]
        data['classifiers'] = classifiers

    # check requires and obsoletes
    def validate_version_predicates(col, sequence):
        try:
            map(versionpredicate.VersionPredicate, sequence)
        except ValueError, message:
            raise ValueError, 'Bad "%s" syntax: %s'%(col, message)
    for col in ('requires', 'obsoletes'):
        if data.has_key(col) and data[col]:
            validate_version_predicates(col, data[col])

    # check provides
    if data.has_key('provides') and data['provides']:
        try:
            map(versionpredicate.check_provision, data['provides'])
        except ValueError, message:
            raise ValueError, 'Bad "provides" syntax: %s'%message

    # check classifiers depending on verifyClassifiers which depends on site
    # settings for checkClassifiersOnVerify and checkClassifiersOnUpload
    if data.has_key('classifiers'):
        d = {}
        for cKey in getClassifierKeys():
            d[cKey] = 1
        cf = {}
        classifiers = data['classifiers']
        if not isinstance(classifiers, types.ListType):
            # huh, only one classifier given
            classifiers = [classifiers]
        for entry in classifiers:
            if d.has_key(entry):
                # only use existent classifiers
                cf[entry] = 1
            elif verifyClassifiers:
                # raise error if defined in site
                raise ValueError, 'Invalid classifier "%s"'%entry
        data['classifiers'] = cf.keys()


# cache this
classifiersDataPath = os.path.join(os.path.dirname(__file__),
    'classifiers.data')

pypiClassifiersURL = 'https://pypi.org/pypi?%3Aaction=list_classifiers'

class ClassifierBuilder(object):
    """ClassifierBuilder."""

    def __init__(self, pypiClassifiersURL=pypiClassifiersURL):
        fData = open(classifiersDataPath)

#        # avoid calling data from pypi
#        import socket
#        try:
#            old_timeout = socket.getdefaulttimeout()
#            socket.setdefaulttimeout(10)
#            try:
#                fData = urllib2.urlopen(pypiClassifiersURL)
#            finally:
#                socket.setdefaulttimeout(old_timeout)
#        except urllib2.URLError:
#            # use the default data if we have no access to pypi
#            fData = open(classifiersDataPath)

        try:
            self._lines = sorted([line.strip() for line in fData.readlines()])
        finally:
            fData.close()
        # setup data dict
        ids = {}
        for line in self._lines:
            split = line.split(' :: ')
            i = -1
            id_, title = self._getIdAndTitle(split[i])
            while id_ in ids:
                i -= 1
                id_ = '%s %s' % (split[i], id_)
                id_, title = self._getIdAndTitle(id_)
            ids[line] = id_, title
        self.data = ids

    def _getIdAndTitle(self, field):
        """Returns id and title."""
        return field.lower().replace(' ', ''), field

    def get(self):
        """Returns data."""
        return self.data

    def keys(self):
        return self.data.keys()

    def values(self):
        return self.data.values()

    def items(self):
        return self.data.items()

    def list(self):
        return self._lines


def getClassifierData():
    # cache this in ram cache for a period given from IPYPISite
    return ClassifierBuilder()

def getClassifierKeys():
    # cache this in ram cache for a period given from IPYPISite
    builder = ClassifierBuilder()
    return builder.keys()

def listClassifiers():
    builder = ClassifierBuilder()
    return builder.list()

# moved from docutils, this is gone in newer docutils
def trim_docstring(text):
    """
    Trim indentation and blank lines from docstring text & return it.

    See PEP 257.
    """
    if not text:
        return text
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = text.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxint
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxint:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return '\n'.join(trimmed)

def formatDescription(source):
    """Pypi description formatter."""
    # trim source
    source = trim_docstring(source)

    settings_overrides={
        'raw_enabled': '0',  # no raw HTML code
        'file_insertion_enabled': '0',  # no file/URL access
        'halt_level': 2,  # at warnings or errors, raise an exception
        'report_level': 5,  # never report problems with the reST code
        }

    # capture publishing errors, they go to stderr
    old_stderr = sys.stderr
    sys.stderr = s = cStringIO.StringIO()
    parts = None
    try:
        # convert reStructuredText to HTML
        parts = publish_parts(source=source, writer_name='html',
                              settings_overrides=settings_overrides)
    except:
        pass

    sys.stderr = old_stderr

    # original text if publishing errors occur
    if parts is None or len(s.getvalue()) > 0:
        output = "".join('<PRE>\n' + source + '</PRE>')
    else:
        output = parts['body']

    return output
