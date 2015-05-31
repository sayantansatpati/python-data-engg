__author__ = 'ssatpati'

import requests
import urllib2
import ssl
import json
import pprint

url = "https://cmpaas.vip.ebay.com/swdeploy/jobs/details/2015-04-06%7CDeployJob.923584f414c0a2a6d7f414e4fffffee4%7CLSDSMraptor?serviceid=/ENVhqh2gk6hi9y3h/nrtraptor-app__ENVhqh2gk6hi9y3h"

ctx = ssl.SSLSocket
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

p = urllib2.HTTPPasswordMgrWithDefaultRealm()

p.add_password(None, url, "_CASSINIQE_CMPAAS", "_CASSINIQE_CMPAAS")
handler = urllib2.HTTPBasicAuthHandler(p)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)

#response = urllib2.urlopen(url)
#j = response.read()
j = requests.get(url, verify=False)
print(j.text)
dj = json.loads(j.text)
pprint.pprint(dj)
