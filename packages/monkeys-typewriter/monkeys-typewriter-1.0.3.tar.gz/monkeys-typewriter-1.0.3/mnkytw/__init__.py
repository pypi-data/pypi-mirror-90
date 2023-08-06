import random
from mnkytw.LiteralMatch import LiteralMatch
from mnkytw.MatchAlternation import MatchAlternation
from mnkytw.MatchJoin import MatchJoin
from mnkytw.MatchQuantity import MatchQuantity
from mnkytw.RegexMatch import RegexMatch

# @body the body to parse (fully)
# @matcher the matcher to use to parse the body
# This function is a helper function designed to execute a matcher
# and test if said matcher fully matches the body
# Generally speaking the matcher should be a document matcher, capable
# of fully parsing and account for all possible ways for expressing your
# language, including appropriate whitespacing
def peg_parse(body : str, matcher):
    result = matcher.parser(body, False)
    if result[1] != len(body):
        return False
    return result[0]

def to_string(matcher):
    return matcher.to_string(random.random())