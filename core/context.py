import re
from itertools import izip

from core.config import TEST_INJCT, eventHandlers, specialTagAttrs

# from core.logging import log <--- do we need a logging module ?

#  we iterate through each instances where the input gets reflected
#  in the response URL
#  We need to search in 3 contexts (possible sub contexts exists as well especially amongst script tags):
#  1. Between/amongst tags      ie.              <tag>TEST_INJCT<tag>
#  2. Inside tag                ie.              <tag attr="TEST_INJCT">
#  3. Inside script section     ie.              <script> ... TEST_INJCT ... </script>

# TODO: refactor to use all camelcase or C-style "_" for variable names, but NOT both

# Context object holds the context in which the TEST_INJCT input is reflected in
# holds 
reflectedContexts = []

class Context:
    def __init__(self, quotes, between_or_inside, html_tag, tag_attribute, paramNum, left, right, script=False):
        self.quotes = quotes
        self.between_or_inside = between_or_inside
        self.html_tag = html_tag
        self.tag_attribute = tag_attribute
        self.script = script
        self.paramNum = paramNum
        self.left = left
        self.right = right

def getContext(res):
    contexts = res.text.split(TEST_INJCT)
    if len(contexts) < 2:
        print "Nothing found"
        return False
    
    # an injection context is comprised of the part preceding
    for left, right in zip(contexts, contexts[1:]):
        quotes = ""
        between_or_inside = ""
        html_tag = "" 
        tag_attribute = ""
        paramNum = right[:1] # since html is split on test string, the paramNumber should be the first character on the RHS

        between_or_inside = parse_between_or_inside(left, right)
        if between_or_inside == "><":
            html_tag = parse_html_tag(left, right)
            if html_tag == "script":
                script = parse_script(left, right)
                if not script:
                    print "Script context not yet supported"
            else: # might need more cases to handle different tags
                # possibly should refactor this
                ctxt = Context(quotes, between_or_inside, html_tag, tag_attribute, paramNum, left, right)
                reflectedContexts.append(ctxt)

        elif between_or_inside == "<>":
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
                ctxt = Context(quotes, between_or_inside, html_tag, tag_attribute, paramNum, left, right)
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

def parse_html_tag(left):
    left = left[::-1]
    # put this in an utils function
    r_index = left.index("<")
    index_dict = {og_index: rev_index for rev_index, og_index in zip(range(len(left), 0, -1), range(0, len(left)))}
    index = index_dict[r_index]

    html = left[index+1:]split()[0]

    print "html >>>>> " + html
    return html
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
    