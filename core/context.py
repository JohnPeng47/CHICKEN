import re
from itertools import izip

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

class Context:
    def __init__(self, quotes, between_or_inside, html_tag, tag_attribute, script=False):
        self.quotes = quotes
        self.between_or_inside = between_or_inside
        self.html_tag = html_tag
        self.tag_attribute = tag_attribute
        self.script = script

def getContext(res):
    contexts = res.text.split(test)
    if len(contexts) < 2:
        print "Nothing found"
        return False
    
    for left, right in zip(contexts, contexts[1:]):
        quotes = ""
        between_or_inside = ""
        html_tag = "" 
        tag_attribute = ""
        between_or_inside = parse_between_or_inside(left, right)
        if between_or_inside == "><": # or "between" ??
            html_tag = parse_html_tag(left, right)
            if html_tag == "script":
                script = parse_script(left, right)
                if not script:
                    print "Script context not yet supported"
            else: # might need more cases to handle different tags
                # possibly should refactor this
                ctxt = Context(quotes, between_or_inside, html_tag, tag_attribute)
                reflectedContexts.append(ctxt)
        elif between_or_inside == "<>": # or "inside" ??
            quotes = parse_single_or_double_quotes(left, right)
            tag_attribute = parse_tag_attribute(left)
            if tag_attribute in eventHandlers: 
                script = parse_script(left, right)
                if not script:
                    print "Script context not yet supported"
                    continue
            elif tag_attribute in specialTagAttrs:
                print "Special attribute not yet handled"
                continue
            else: # test lands inside a regular attribute 
                ctxt = Context(quotes, between_or_inside, html_tag, tag_attribute)
                reflectedContexts.append(ctxt)       
        else:
            continue
            print "Fatal error parsing context"
    
    return reflectedContexts

def parse_script_ctxt():
    pass

# TODO: reimplement this
def parse_tag_attribute(left):
    location = left[:left.rfind("=")].split()
    return location[len(location) - 1]

def find_first(ctxt, char1, char2, reverse = False):
    if reverse:
        ctxt = ctxt[::-1]    
    for c in ctxt:
        if c == char1:
            return char1
        elif c == char2:
            return char2
    return False

# below two functions are similiar in structure, could be changed
def parse_single_or_double_quotes(left, right):
    left_quote = find_first(left, "\'", "\"", reverse = True)
    right_quote = find_first(right, "\'", "\"", reverse = False)

    if left_quote == "\'" and right_quote == "\'":
         return "\'" 
    elif left_quote == "\"" and right_quote == "\"":
        return "\""
    else:
        return False

def parse_between_or_inside(left, right):
    left_tag = find_first(left, "<", ">", reverse = True)
    right_tag = find_first(right, "<", ">", reverse = False)

    if left_tag == "<" and right_tag == ">":
        return "<>"
    elif left_tag == ">" and right_tag == "<":
        return "><"
    else:
        return False
    