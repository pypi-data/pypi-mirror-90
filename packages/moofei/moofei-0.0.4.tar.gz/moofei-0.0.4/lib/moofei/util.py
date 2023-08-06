#!/usr/bin/python
# coding: utf-8
# editor: mufei(ypdh@qq.com tel:15712150708)
'''
牧飞 _ __ ___   ___   ___  / _| ___(_)
| '_ ` _ \ / _ \ / _ \| |_ / _ \ |
| | | | | | (_) | (_) |  _|  __/ |
|_| |_| |_|\___/ \___/|_|  \___|_|
'''

__all__ = ['urlopen', 'urlparse', 'tldextract']

import sys, os
py = list(sys.version_info)


if py[0]==2:
    #url, data=None, timeout=<object>, cafile=None, capath=None, cadefault=False, context=None
    from urllib2 import urlopen
    from urlparse import urlparse
else:
    #url, data=None, timeout=<object>, *, cafile=None, capath=None, cadefault=False, context=None
    from urllib.request import urlopen
    from urllib.parse import urlparse
    
    
try:
   import tldextract
except:
   tldextract = None


   
  