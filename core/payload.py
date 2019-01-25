from core.config import WSpayload, specialTagAttrs

def genPayload(ctxt):
    print WSpayload
    payload = "" 
    if ctxt.between_or_inside == "<>":
        if ctxt.tag_attribute not in specialTagAttrs and not ctxt.script:
            if ctxt.quotes == "\"":
                payload = 