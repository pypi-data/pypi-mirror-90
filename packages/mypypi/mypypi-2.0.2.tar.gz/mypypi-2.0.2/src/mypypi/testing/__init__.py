##############################################################################
#
# Copyright (c) 2018 Projekt01 GmbH and Contributors.
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

import os
import json as _json
import time
import shutil
import urllib2
import StringIO
import doctest
try:
    from hashlib import md5
except ImportError:
    from md5 import md5

import mypypi.api

import p01.tmp.storage
import p01.fsfile.storage

from zope.app.testing import setup
from zope.app.testing import functional

import p01.checker


###############################################################################
#
# source code checker (without CSS validation)
#
###############################################################################

CHECKERS = {
    'html': p01.checker.PT_CHECKERS,
    'jpg': p01.checker.JPG_CHECKERS,
    'png': p01.checker.PNG_CHECKERS,
    'js': p01.checker.JS_CHECKERS,
    'po': p01.checker.PO_CHECKERS,
    'pt': p01.checker.PT_CHECKERS,
    'py': p01.checker.PY_CHECKERS,
    'txt': p01.checker.TXT_CHECKERS,
    'zcml': p01.checker.ZCML_CHECKERS,
}

def check(module, domainPath='/', domains=('mypypi',), skipFileNames=[],
    skipFolderNames=[], checkers=CHECKERS):
    checker = p01.checker.Checker(checkers=checkers)
    zcmlChecker = p01.checker.ZCMLBadI18nDomainChecker(domainPath, domains)
    checker.addChecker('zcml', zcmlChecker)
    ptChecker = p01.checker.PTBadI18nDomainChecker(domainPath, domains)
    checker.addChecker('pt', ptChecker)
    checker.check(module, skipFileNames=skipFileNames,
        skipFolderNames=skipFolderNames)

###############################################################################
#
# helper
#
###############################################################################

def doRemoveTree(src, sleep=5, retry=0):
    while retry <= 3:
        retry += 1
        try:
            if os.path.exists(src):
                shutil.rmtree(src)
        except Exception, e: # WindowsError, OSError?, just catch anything
            # this was to early just try again
            time.sleep(sleep)
            doRemoveTree(src, sleep, retry)
        # break while if everything is fine
        break

###############################################################################
#
# Test Component
#
###############################################################################

#put here some testing globals
#those will be filled by default with good values
#it will be real easy to mess these up in testcases to produce some failures

Z3C_PKG_SIMPLE_RESPONSE = """<html>
<head><title>z3c.form</title>
</head>
<body>
<h1>z3c.form</h1>
<a href="http://localhost/z3c.form/1.0.0/z3c.form-1.0.0-py2.4.egg">z3c.form-1.0.0-py2.4.egg</a><br />
<a href="http://localhost/z3c.form/1.0.0/z3c.form-1.0.0.tar.gz">z3c.form-1.0.0.tar.gz</a><br />
<a href="http://localhost/z3c.form/1.0c1/z3c.form-1.0c1-py2.4.egg">z3c.form-1.0c1-py2.4.egg</a><br />
<a href="http://localhost/z3c.form/1.0c1/z3c.form-1.0c1.tar.gz">z3c.form-1.0c1.tar.gz</a><br />
<a href="http://localhost/z3c.form/1.0c2/z3c.form-1.0c2-py2.4.egg">z3c.form-1.0c2-py2.4.egg</a><br />
<a href="http://localhost/z3c.form/1.0c2/z3c.form-1.0c2.tar.gz">z3c.form-1.0c2.tar.gz</a><br />
<a href="http://localhost/z3c.form/1.1.0/z3c.form-1.1.0-py2.4.egg">z3c.form-1.1.0-py2.4.egg</a><br />
<a href="http://localhost/z3c.form/1.1.0/z3c.form-1.1.0.tar.gz">z3c.form-1.1.0.tar.gz</a><br />
<a href="http://localhost/z3c.form/1.2.0/z3c.form-1.2.0-py2.4.egg">z3c.form-1.2.0-py2.4.egg</a><br />
<a href="http://localhost/z3c.form/1.2.0/z3c.form-1.2.0.tar.gz">z3c.form-1.2.0.tar.gz</a><br />
<a href="http://localhost/z3c.form/1.3.0/z3c.form-1.3.0-py2.4.egg">z3c.form-1.3.0-py2.4.egg</a><br />
<a href="http://localhost/z3c.form/1.3.0/z3c.form-1.3.0.tar.gz">z3c.form-1.3.0.tar.gz</a><br />
<a href="http://localhost/z3c.form/1.4.0/z3c.form-1.4.0-py2.4.egg">z3c.form-1.4.0-py2.4.egg</a><br />
<a href="http://localhost/z3c.form/1.4.0/z3c.form-1.4.0.tar.gz">z3c.form-1.4.0.tar.gz</a><br />
<a href="http://localhost/z3c.form/1.4.0b1/z3c.form-1.4.0b1-py2.4.egg">z3c.form-1.4.0b1-py2.4.egg</a><br />
<a href="http://localhost/z3c.form/1.4.0b1/z3c.form-1.4.0b1.tar.gz">z3c.form-1.4.0b1.tar.gz</a><br />
<a href="http://localhost/z3c.form/1.5.0/z3c.form-1.5.0-py2.4.egg">z3c.form-1.5.0-py2.4.egg</a><br />
<a href="http://localhost/z3c.form/1.5.0/z3c.form-1.5.0.tar.gz">z3c.form-1.5.0.tar.gz</a><br />
<a href="http://localhost/z3c.form/1.5.0b1/z3c.form-1.5.0b1-py2.4.egg">z3c.form-1.5.0b1-py2.4.egg</a><br />
<a href="http://localhost/z3c.form/1.5.0b1/z3c.form-1.5.0b1.tar.gz">z3c.form-1.5.0b1.tar.gz</a><br />
<a href="http://localhost/z3c.form/1.6.0/z3c.form-1.6.0-py2.4.egg">z3c.form-1.6.0-py2.4.egg</a><br />
<a href="http://localhost/z3c.form/1.6.0/z3c.form-1.6.0.tar.gz">z3c.form-1.6.0.tar.gz</a><br />
<a href="http://localhost/z3c.form/1.7.0/z3c.form-1.7.0.tar.gz">z3c.form-1.7.0.tar.gz</a><br />
<a href="http://localhost/z3c.form/1.8.0/z3c.form-1.8.0.tar.gz">z3c.form-1.8.0.tar.gz</a><br />
<a href="http://localhost/z3c.form/1.8.1/z3c.form-1.8.1.tar.gz">z3c.form-1.8.1.tar.gz</a><br />
<a href="http://localhost/z3c.form/1.8.2/z3c.form-1.8.2.tar.gz">z3c.form-1.8.2.tar.gz</a><br />
<a href="http://localhost/z3c.form/1.9.0/z3c.form-1.9.0.tar.gz">z3c.form-1.9.0.tar.gz</a><br />
<a href="http://localhost/z3c.form/2.0.0/z3c.form-2.0.0.tar.gz">z3c.form-2.0.0.tar.gz</a><br />
<a href="http://localhost/z3c.form/3.0/z3c.form-3.0.zip">z3c.form-3.0.zip</a><br />
<a href="http://localhost/z3c.form/3.1.0/z3c.form-3.1.0.zip">z3c.form-3.1.0.zip</a><br />
<a href="http://localhost/z3c.form/3.2.0/z3c.form-3.2.0.zip">z3c.form-3.2.0.zip</a><br />
<a href="http://localhost/z3c.form/3.3.0/z3c.form-3.3.0.tar.gz">z3c.form-3.3.0.tar.gz</a><br />
<a href="http://localhost/z3c.form/3.4.0/z3c.form-3.4.0.tar.gz">z3c.form-3.4.0.tar.gz</a><br />
<a href="http://localhost/z3c.form/3.5/z3c.form-3.5.tar.gz">z3c.form-3.5.tar.gz</a><br />
<a href="http://localhost/z3c.form/3.6/z3c.form-3.6.tar.gz">z3c.form-3.6.tar.gz</a><br />
<a href="http://localhost/z3c.form/3.7.0/z3c.form-3.7.0-py2.py3-none-any.whl">z3c.form-3.7.0-py2.py3-none-any.whl</a><br />
<a href="http://localhost/z3c.form/4.0/z3c.form-4.0.tar.gz">z3c.form-4.0.tar.gz</a><br />
</body>
</html>
<BLANKLINE>
"""

WSGI_INTERCEPT_SIMPLE_RESPONSE = """<html>
<head>
<base href="http://localhost/simple/wsgi-intercept" />
<title>wsgi-intercept</title>
</head>
<body>
<h1>wsgi-intercept</h1>
<a href="http://localhost/wsgi-intercept/0.10.0/wsgi_intercept-0.10.0.tar.gz">wsgi_intercept-0.10.0.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/0.10.1/wsgi_intercept-0.10.1.tar.gz">wsgi_intercept-0.10.1.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/0.10.2/wsgi_intercept-0.10.2.tar.gz">wsgi_intercept-0.10.2.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/0.10.3/wsgi_intercept-0.10.3.tar.gz">wsgi_intercept-0.10.3.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/0.3/wsgi_intercept-0.3-py2.4.egg">wsgi_intercept-0.3-py2.4.egg</a><br />
<a href="http://localhost/wsgi-intercept/0.3/wsgi_intercept-0.3.tar.gz">wsgi_intercept-0.3.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/0.3.1/wsgi_intercept-0.3.1-py2.4.egg">wsgi_intercept-0.3.1-py2.4.egg</a><br />
<a href="http://localhost/wsgi-intercept/0.3.1/wsgi_intercept-0.3.1.tar.gz">wsgi_intercept-0.3.1.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/0.3.2/wsgi_intercept-0.3.2-py2.4.egg">wsgi_intercept-0.3.2-py2.4.egg</a><br />
<a href="http://localhost/wsgi-intercept/0.3.2/wsgi_intercept-0.3.2.tar.gz">wsgi_intercept-0.3.2.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/0.3.3/wsgi_intercept-0.3.3-py2.4.egg">wsgi_intercept-0.3.3-py2.4.egg</a><br />
<a href="http://localhost/wsgi-intercept/0.3.3/wsgi_intercept-0.3.3.tar.gz">wsgi_intercept-0.3.3.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/0.3.4/wsgi_intercept-0.3.4-py2.4.egg">wsgi_intercept-0.3.4-py2.4.egg</a><br />
<a href="http://localhost/wsgi-intercept/0.3.4/wsgi_intercept-0.3.4-py2.5.egg">wsgi_intercept-0.3.4-py2.5.egg</a><br />
<a href="http://localhost/wsgi-intercept/0.3.4/wsgi_intercept-0.3.4.tar.gz">wsgi_intercept-0.3.4.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/0.4/wsgi_intercept-0.4-py2.5.egg">wsgi_intercept-0.4-py2.5.egg</a><br />
<a href="http://localhost/wsgi-intercept/0.4/wsgi_intercept-0.4.tar.gz">wsgi_intercept-0.4.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/0.5.0/wsgi_intercept-0.5.0.tar.gz">wsgi_intercept-0.5.0.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/0.5.1/wsgi_intercept-0.5.1.tar.gz">wsgi_intercept-0.5.1.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/0.6.0/wsgi_intercept-0.6.0.tar.gz">wsgi_intercept-0.6.0.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/0.6.1/wsgi_intercept-0.6.1.tar.gz">wsgi_intercept-0.6.1.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/0.6.2/wsgi_intercept-0.6.2.tar.gz">wsgi_intercept-0.6.2.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/0.6.3/wsgi_intercept-0.6.3.tar.gz">wsgi_intercept-0.6.3.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/0.6.4/wsgi_intercept-0.6.4.tar.gz">wsgi_intercept-0.6.4.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/0.6.5/wsgi_intercept-0.6.5.tar.gz">wsgi_intercept-0.6.5.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/0.7.0/wsgi_intercept-0.7.0.tar.gz">wsgi_intercept-0.7.0.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/0.8.0/wsgi_intercept-0.8.0.tar.gz">wsgi_intercept-0.8.0.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/0.8.1/wsgi_intercept-0.8.1.tar.gz">wsgi_intercept-0.8.1.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/0.9.0/wsgi_intercept-0.9.0.tar.gz">wsgi_intercept-0.9.0.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/0.9.1/wsgi_intercept-0.9.1.tar.gz">wsgi_intercept-0.9.1.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/1.0.0/wsgi_intercept-1.0.0.tar.gz">wsgi_intercept-1.0.0.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/1.0.1/wsgi_intercept-1.0.1.tar.gz">wsgi_intercept-1.0.1.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/1.1.0/wsgi_intercept-1.1.0.tar.gz">wsgi_intercept-1.1.0.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/1.1.1/wsgi_intercept-1.1.1.tar.gz">wsgi_intercept-1.1.1.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/1.1.2/wsgi_intercept-1.1.2.tar.gz">wsgi_intercept-1.1.2.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/1.1.3/wsgi_intercept-1.1.3.tar.gz">wsgi_intercept-1.1.3.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/1.2.0/wsgi_intercept-1.2.0.tar.gz">wsgi_intercept-1.2.0.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/1.2.2/wsgi_intercept-1.2.2.tar.gz">wsgi_intercept-1.2.2.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/1.3.0/wsgi_intercept-1.3.0.tar.gz">wsgi_intercept-1.3.0.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/1.3.1/wsgi_intercept-1.3.1.tar.gz">wsgi_intercept-1.3.1.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/1.3.2/wsgi_intercept-1.3.2.tar.gz">wsgi_intercept-1.3.2.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/1.4.0/wsgi_intercept-1.4.0.tar.gz">wsgi_intercept-1.4.0.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/1.4.1/wsgi_intercept-1.4.1.tar.gz">wsgi_intercept-1.4.1.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/1.5.0/wsgi_intercept-1.5.0.tar.gz">wsgi_intercept-1.5.0.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/1.5.1/wsgi_intercept-1.5.1.tar.gz">wsgi_intercept-1.5.1.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/1.6.0/wsgi_intercept-1.6.0.tar.gz">wsgi_intercept-1.6.0.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/1.7.0/wsgi_intercept-1.7.0.tar.gz">wsgi_intercept-1.7.0.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/1.8.0/wsgi_intercept-1.8.0-py2.py3-none-any.whl">wsgi_intercept-1.8.0-py2.py3-none-any.whl</a><br />
<a href="http://localhost/wsgi-intercept/1.8.0/wsgi_intercept-1.8.0.tar.gz">wsgi_intercept-1.8.0.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/1.8.1/wsgi_intercept-1.8.1-py2.py3-none-any.whl">wsgi_intercept-1.8.1-py2.py3-none-any.whl</a><br />
<a href="http://localhost/wsgi-intercept/1.8.1/wsgi_intercept-1.8.1.tar.gz">wsgi_intercept-1.8.1.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/1.9.0/wsgi_intercept-1.9.0-py2.py3-none-any.whl">wsgi_intercept-1.9.0-py2.py3-none-any.whl</a><br />
<a href="http://localhost/wsgi-intercept/1.9.0/wsgi_intercept-1.9.0.tar.gz">wsgi_intercept-1.9.0.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/1.9.1/wsgi_intercept-1.9.1-py2.py3-none-any.whl">wsgi_intercept-1.9.1-py2.py3-none-any.whl</a><br />
<a href="http://localhost/wsgi-intercept/1.9.1/wsgi_intercept-1.9.1.tar.gz">wsgi_intercept-1.9.1.tar.gz</a><br />
<a href="http://localhost/wsgi-intercept/1.9.2/wsgi_intercept-1.9.2-py2.py3-none-any.whl">wsgi_intercept-1.9.2-py2.py3-none-any.whl</a><br />
<a href="http://localhost/wsgi-intercept/1.9.2/wsgi_intercept-1.9.2.tar.gz">wsgi_intercept-1.9.2.tar.gz</a>
</body>
</html>
<BLANKLINE>
"""

Z3C_FORM_JSON_RESPONSE = os.path.join(os.path.dirname(__file__),
    'z3c-form-json.txt')

WSGI_INTERCEPT_JSON_RESPONSE = os.path.join(os.path.dirname(__file__),
    'wsgi-intercept-json.txt')


class FakeRequestsRequest(object):
    """Fake requests Request"""

    def __init__(self, method=None, url=None, headers=None, body=None):
        self.method = method
        self.url = url
        self.headers = headers
        self.body = body


class FakeRequestsResponse(object):
    """Fake requests response

    Enhance this class if you need more then the json method.
    """

    content = None
    headers = {}
    status_code = 200

    def __init__(self, content, status_code=200, method=None, url=None,
        headers=None, body=None):
        self.content = content
        self.headers = headers
        self.status_code = status_code
        self.request = FakeRequestsRequest(method, url, headers, body)

    @property
    def ok(self):
        if self.status_code == 200:
            return True
        else:
            return False

    def json(self):
        return _json.loads(self.content)

    def get(self, key):
        # incomplete for several usecases
        return self.json().get(key)


class FakeRequestsSessionFactory(object):
    """Fake request session factory"""

    adapters = {}

    def __init__(self):
        self.adapters = {}

    def request(self, method, url, headers=None, params=None, data=None,
        json=None, proxies=None, verify=False):
        #use this method instead of urllib2.urlopen
        #we can return a StringIO or raise urllib2.HTTPError
        if url == 'https://pypi.org/pypi/z3c.form/json':
            f = open(Z3C_FORM_JSON_RESPONSE, 'rb')
            content = f.read()
            f.close()
            return FakeRequestsResponse(content)
        elif url == 'https://pypi.org/pypi/wsgi-intercept/json':
            f = open(WSGI_INTERCEPT_JSON_RESPONSE, 'rb')
            content = f.read()
            f.close()
            return FakeRequestsResponse(content)
        elif url == 'http://localhost/simple/z3c.form':
            return FakeRequestsResponse(Z3C_PKG_SIMPLE_RESPONSE)
        elif url == 'http://localhost/simple/wsgi-intercept':
            return FakeRequestsResponse(WSGI_INTERCEPT_SIMPLE_RESPONSE)
        else:
            content = 'TGZ--PACKAGE-FILE_DATA--ENDTGZ'
            return FakeRequestsResponse(content)



###############################################################################
#
# setup helper
#
###############################################################################

# _orgPYPIPRoxyConnectionClass = None

# def setUpFakeXMLRPCPYPI(test):
#     global _orgPYPIPRoxyConnectionClass
#     _orgPYPIPRoxyConnectionClass = mypypi.api._connectionClass
#     mypypi.api._connectionClass = FakeXMLRPCPYPI


# def tearDownFakeXMLRPCPYPI(test):
#     mypypi.api._connectionClass = _orgPYPIPRoxyConnectionClass


# _orgUrlOpener = None
_orgRequestsSessionFactory = None

def setUpFakeRequestsFactory(test):
    # global _orgUrlOpener
    # _orgUrlOpener = mypypi.api._urlopen
    # mypypi.api._urlopen = fakeUrlOpener
    global _orgRequestsSessionFactory
    _orgRequestsSessionFactory = mypypi.api.APIClient._sessionFactory
    mypypi.api.APIClient._sessionFactory = FakeRequestsSessionFactory

def tearDownFakeRequestsFactory(test):
    # mypypi.api._urlopen = _orgUrlOpener
    mypypi.api.APIClient._sessionFactory = _orgRequestsSessionFactory


###############################################################################
#
# placeful setup/teardown
#
###############################################################################

def placefulSetUp(test):
    site = setup.placefulSetUp(site=True)
    test.globs['rootFolder'] = site
    # setUpFakeXMLRPCPYPI(test)


def placefulTearDown(test):
    setup.placefulTearDown()
    # tearDownFakeXMLRPCPYPI(test)


def placefulSetUpWithRealXMLRPC(test):
    site = setup.placefulSetUp(site=True)
    test.globs['rootFolder'] = site


def placefulTearDownWithRealXMLRPC(test):
    setup.placefulTearDown()


###############################################################################
#
# functional layer
#
###############################################################################

def getRootFolder():
    return functional.FunctionalTestSetup().getRootFolder()

def cleanFSFolders():
    p1 = p01.tmp.storage.getTMPStoragePath()
    for name in os.listdir(p1):
        dName = os.path.join(p1, name)
        doRemoveTree(dName)
    p2 = p01.fsfile.storage.getFSStoragePath()
    for name in os.listdir(p2):
        dName = os.path.join(p2, name)
        doRemoveTree(dName)
    time.sleep(1)

def doctestSetUp(test):
    cleanFSFolders()
    # implement fake server and support basic methods
    setUpFakeRequestsFactory(test)

def doctestTearDown(test):
    cleanFSFolders()
    # implement fake server and support basic methods
    tearDownFakeRequestsFactory(test)

FTESTING_ZCML = os.path.join(os.path.dirname(__file__), 'ftesting.zcml')
FTESTING_ZCML = os.path.abspath(FTESTING_ZCML)

PYPIFunctionalLayer = functional.ZCMLLayer(FTESTING_ZCML, __name__, 'Functional')

def FunctionalDocFileSuite(path, **kw):
    """Including relative path setup."""
    globs = {'getRootFolder': getRootFolder}
    if 'globs' in kw:
        globs.update(kw['globs'])
        del kw['globs']

    kw['setUp'] = kw.get('setUp', doctestSetUp)
    kw['tearDown'] = kw.get('tearDown', doctestTearDown)
    kw['optionflags'] = kw.get('optionflags',
                               doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

    if 'package' not in kw:
        kw['package'] = doctest._normalize_module(kw.get('package', None))
    kw['module_relative'] = kw.get('module_relative', True)

    suite = functional.FunctionalDocFileSuite(
            path,
            globs=globs,
            **kw)

    suite.layer = PYPIFunctionalLayer
    return suite