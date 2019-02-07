import requests
import re

from config import filtered_inputs, TEST_INJCT, headers
from utils import get_key_from_val

# TODO: needs to handle case where reflected input is intentionally different than original
# ie. in the case of null characters for padding etc.
def testFilter(url, param, test_input):
    #TODO: regex bruteforcing
    data = {
        param : "FINDME" + test_input + "FINDME"
    }
    # regex doesn't work for some reason?
    # reflected = re.match(r'FINDME(.*)FINDME', res.text)
    # print reflected.group(0)
    res = requests.get(url, headers=headers, params=data)
    if res.status_code == 404:
        print "Blocked by WAF"
        return None

    reflected = res.text.split("FINDME")[1]
    
    # works for now but we need to also account for cases of html encoding
    # and escaping our input
    filtered = []
    for char in filtered_inputs:
        if char not in reflected:
            print "{} is filtered".format(char)
            filtered.append(char)

    return filtered
