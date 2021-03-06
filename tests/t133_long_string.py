#!/usr/bin/env python

from runtest import TestBase

class TestCase(TestBase):
    def __init__(self):
        TestBase.__init__(self, 'hello', """
# DURATION    TID     FUNCTION
  62.202 us [28141] | __cxa_atexit();
            [28141] | main() {
   2.405 us [28141] |   printf("Hello %s\\n", "0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789");
   3.005 us [28141] | } /* main */
""")

    def build(self, name, cflags='', ldflags=''):
        # cygprof doesn't support arguments now
        if cflags.find('-finstrument-functions') >= 0:
            return TestBase.TEST_SKIP

        return TestBase.build(self, name, cflags, ldflags)

    def runcmd(self):
        return '%s -A printf@arg1/s,arg2/s -A __printf_chk@arg2/s,arg3/s %s %s' % \
            (TestBase.ftrace, 't-' + self.name, "0123456789" * 10)

    def fixup(self, cflags, result):
        return result.replace('printf', '__printf_chk')
