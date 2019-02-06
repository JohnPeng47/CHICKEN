import requests
import re

from config import filtered_inputs, TEST_INJCT, headers
from utils import get_key_from_val

def testFilter(url, ctxts, params):
    ctx = ctxts[3] # only need to test one parameter
    
    param = get_key_from_val(TEST_INJCT + ctx.paramNum, params)
    if not param:
        print "Not valid 1st param"
        return None    

    #TODO: regex bruteforcing
    test_input = "".join(filtered_inputs)
    data = {
        param : "FINDME" + test_input + "FINDME"
    }
    # regex doesn't work for some reason?
    # reflected = re.match(r'FINDME(.*)FINDME', res.text)
    # print reflected.group(0)
    res = requests.get(url, headers=headers, params=data)
    reflected = res.text.split("FINDME")[1]
    
    filtered = []
    for char in filtered_inputs:
        if char not in reflected:
            print "{} is filtered".format(char)

    return filtered
