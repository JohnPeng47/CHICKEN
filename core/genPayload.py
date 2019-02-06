from core.config import specialTagAttrs
from core.payloads import WSpayload, DOUBLE_QUOTE_ATTR, SINGLE_QUOTE_ATTR, SVG_VECTOR

def genPayload(ctxt, filtered):
    payload = "" 
    context = ""
    if ctxt.between_or_inside == "<>":
        if ctxt.tag_attribute not in specialTagAttrs and not ctxt.script:
            quotes = BREAK_DOUBLE_QUOTES if ctxt.quotes == "\"" else BREAK_SINGLE_QUOTE
            payload = quotes + SVG_VECTOR(WSpayload)
            
    
    return payload

def 