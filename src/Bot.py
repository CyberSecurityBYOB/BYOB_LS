#! /usr/bin/env python

from ConfigurationFileReader import ConfigurationFileReader
from urllib2 import Request, URLError, urlopen, HTTPError

# Read file
fileReader = ConfigurationFileReader()
fileReader.readConfigurationFile()

# Prepare request
# Valid URL url = 'http://www.google.com'
# Unreachable URL url = 'http://www.asjdsajdsakjdsaksadjkasd.com'
# Invalid URL url = 'dsakjshdakjadshksdahjksad'
url = 'http://www.google.com'
#headers = {'User-Agent' : 'Mozilla 5.10'}
#request = urllib2.Request(url, None, headers)
request = Request(url)
request.add_header('User-agent', 'Mozilla 5.10')

# Getting the response
try:
    response = urlopen(request)
    # Print the headers
    print response.headers
except URLError, e:
    if hasattr(e,'code') :
        print 'Error code : ' , e.code
    if hasattr(e, 'reason') :
        print 'Error reason  : ' , e.reason
except ValueError, v:
    print 'This URL is invalid'

