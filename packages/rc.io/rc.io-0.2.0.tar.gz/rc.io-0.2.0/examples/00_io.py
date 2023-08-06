#!/usr/bin/env python3

__author__    = 'RADICAL-Consulting'
__email__     = 'devel@radical-consulting.com'
__copyright__ = 'Copyright date 2019-2021'
__license__   = 'LGPL.v3 *or* commercial license'


import sys
import requests

import rc.io


# ------------------------------------------------------------------------------
#
# This example is semantically and syntactically normative for the Proxy and
# Tunnel classes.
#
if __name__ == '__main__':

  # p1 = rc.io.Proxy(pid='two',   url='ssh://two.radical-consulting.com/')
  # p1 = rc.io.Proxy(pid='test',  url='ssh://test@localhost/')
    p1 = rc.io.Proxy(pid='local', url='sh://localhost/')
    print((p1.cmd('hostname -f; hostname -i')))
    sys.exit(0)

    t1 = p1.tunnel('http://ip.jsontest.com/')
    print((t1.url))
    print((requests.get(t1.url)))

    p2 = p1.hop('ssh://one.radical-consulting.com')
    print()
    print((p2.url))
    print((p2.cmd('hostname -f; hostname -i')))

    t2 = p2.tunnel('http://ip.jsontest.com/')
    print((t2.url))
    print((requests.get(t2.url)))


# ------------------------------------------------------------------------------


