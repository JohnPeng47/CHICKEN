from itertools import izip

from core.payload import genPayload
from core.config import test, eventHandlers, specialTagAttrs

# from core.logging import log <--- do we need a logging module ?

#  we iterate through each instances where the input gets reflected
#  in the response URL
#  We need to search in 3 contexts (possible sub contexts exists as well especially amongst script tags):
#  1. Between/amongst tags      ie.              <tag>TEST<tag>
#  2. Inside tag                ie.              <tag attr="TEST">
#  3. Inside script section     ie.              <script> ... TEST ... </script>

# TODO: refactor to use all camelcase or C-style "_" for variable names, but NOT both

# Context object holds the context in which the test input is reflected in
# holds 
reflectedContexts = []
Context = {
    "between_or_inside" :  
}

def getContext(res):
    contexts = res.text.split(test)
    if len(contexts) < 2:
        print "Nothing found"
        return False
    
    for left, right in zip(contexts, contexts[1:]):
        # following makeup the context
        quotes = ""
        between_or_inside = ""
        html_tag = ""
        tag_attribute = ""
        # TODO: add script parsing stuff

        # start from the end of beginning and look for 
        between_or_inside = parse_between_or_inside(left, right)
        if between_or_inside == "><": # or "between" ??
            html_tag = parse_html_tag(left, right)
            if html_tag == "script":
                script = parse_script(left, right)
                if not script:
                    print "Script context not yet supported"
            
            else: # might need more cases to handle different tags
                

        elif between_or_inside == "<>": # or "inside" ??
            quotes = parse_single_or_double_quotes(begin, end)
            tag_attribute = parse_tag_attribute()
            if tag_attribute in eventHandlers: 
                script = parse_script(left, right)
                if not script:
                    print "Script context not yet supported"
            elif tag_attribute in specialTagAttrs:
                gen
            else:
                
                
        else:
            print "Fatal error parsing context"

def parse_script_ctxt():
    return False

def find_first(left, char1, char2, reverse = False):
    
def between_or_inside(left, right):
    left_tag = find_first(left, "<", ">", reverse = True)
    right_tag = find_first(right, "<", ">", reverse = False)

    if left_tag == "<" and right_tag == ">":
        return "<>"
    elif left_tag == ">" and right_tag == "<":
        return "><"
    else:
        return False
    