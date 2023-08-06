# MatchAlternation takes a list of matchers and tries them in order
# until one matches the given body. 
# Note that because we don't enforce strict end matching, MatchAlternation 
# will act greedily essentially using the first # match and consuming as 
# much as possible with that match
class MatchAlternation:
    # @matchers A list of matchers in the order to attempt matching
    def __init__(self, matchers : list):
        self.to_string_call_count = None
        self.matchers = matchers
    
    # @body The body we are matching tokens to in parsing
    # @hard_fail A boolean flag indicating if a matcher should throw an error (or just return false)
    # This method parses a body of text for tokens
    def parser(self, body : str, hard_fail = True):
        for matcher in self.matchers:
            result = matcher.parser(body, hard_fail = False)
            if result:
                return result
        if hard_fail:
            raise ValueError(f"MatchAlternation: Could not match")
        else: 
            return False

    # @call_count A nonce used to detect recursion
    def to_string(self, call_count = 0):
        if self.to_string_call_count == call_count:
            return "..."
        else:
            self.to_string_call_count = call_count
            return "(" + " / ".join([str(m) for m in self.matchers]) + ")"

    def __str__(self):
        return self.to_string(self)