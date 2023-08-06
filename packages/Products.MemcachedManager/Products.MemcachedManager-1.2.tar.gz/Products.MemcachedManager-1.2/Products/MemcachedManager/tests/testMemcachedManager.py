# -*- coding: utf-8 -*-
# Copyright (c) 2004 Zope Corporation and Plone Solutions
# ZPL 2.1 license

from Products.MemcachedManager.MemcachedManager import Memcached
from Products.MemcachedManager.tests import mcmtc

import time


class TestMemcachedManager(mcmtc.MemcachedManagerTestCase):
    """ Test MemcachedManager """

    def testCacheManagerPresence(self):
        cm = self._cachemanager
        self.assertTrue(cm)

    def testCachePresence(self):
        cache = self._cache
        self.assertTrue(cache)

    def testCache_get_counter_value(self):
        cache = self._cache
        ob = self._script
        with self.assertRaises(AttributeError):
            getattr(ob, cache.cachecountervariable)
        value = cache._get_counter_value(ob=ob)
        self.assertIsInstance(value, int)
        self.assertEqual(value, getattr(ob, cache.cachecountervariable))

    def testCacheSetGet(self):
        cache = self._cache
        ob = self._script
        data = "test"
        cache.ZCache_set(ob=ob, data=data)
        self.dummySleep()
        cached = cache.ZCache_get(ob=ob)
        self.assertEqual(cached, data)

    def testCacheInvalidate(self):
        cache = self._cache
        ob = self._script
        data = "test"
        cache.ZCache_set(ob=ob, data=data)
        time.sleep(0.5)
        cache.ZCache_invalidate(ob=ob)
        self.dummySleep()
        self.assertFalse(cache.ZCache_get(ob=ob))

    def testCacheInvalidateMirrors(self):
        cm = self._cachemanager
        cache = self._cache
        ob = self._script
        data = "test"

        mirror = Memcached()
        settings = cm.getSettings()
        mirror.initSettings(settings)
        mirror.initSettings(kw=dict(servers=("127.0.0.1:11111",), mirrors=()))

        cache.ZCache_set(ob=ob, data=data)
        mirror.ZCache_set(ob=ob, data=data)

        time.sleep(0.5)
        # Switch connections, make regular cache the mirror
        cache.initSettings(
            kw=dict(servers=("127.0.0.1:11211",), mirrors=(("127.0.0.1:11111",)))
        )

        cache.ZCache_invalidate(ob=ob)
        self.dummySleep()
        self.assertFalse(cache.ZCache_get(ob=ob))
        self.assertFalse(mirror.ZCache_get(ob=ob))

    def testCacheCleanup(self):
        cache = self._cache
        ob = self._script
        data = "test"
        cache.ZCache_set(ob=ob, data=data)
        self.dummySleep()
        cache.cleanup()
        self.dummySleep()
        self.assertFalse(cache.ZCache_get(ob=ob))

    def testMaxAge(self):
        self.setMaxAge(1)
        self.setRefreshInterval(1)
        cache = self._cache
        ob = self._script
        data = "test"
        self.dummySleep()
        cache.ZCache_set(ob=ob, data=data)
        self.dummySleep(1)
        time.sleep(1)
        # Expired after 1 second
        res = cache.ZCache_get(ob=ob)
        self.assertFalse(res, "Got %s, expected None" % res)

    def testLastmod(self):
        cache = self._cache
        ob = self._script
        data = "test"
        self.dummySleep()
        cache.ZCache_set(ob=ob, data=data)
        self.dummySleep(1)
        time.sleep(1)
        # Last modified updated - should get None
        res = cache.ZCache_get(ob=ob, mtime_func=time.time)
        self.assertFalse(res, "Got %s, expected None" % res)
        # Make sure entry is deleted when expired
        res = cache.ZCache_get(ob=ob, mtime_func=None)
        self.assertFalse(
            res, "Got %s, expected None - entry not deleted on expiry" % res
        )

    def testCacheAcquisitionWrapper(self):
        # Test for hash key conflict
        cache = self._cache
        ob = self._script
        data = self.folder
        self.dummySleep()
        # This is supposed to thrown a TypeError
        # cache.ZCache_set(ob=ob, data=data)
        self.assertRaises(TypeError, cache.ZCache_set, ob=ob, data=data)
        self.dummySleep(1)


def test_suite():
    from unittest import makeSuite
    from unittest import TestSuite

    suite = TestSuite()
    suite.addTest(makeSuite(TestMemcachedManager))
    return suite
