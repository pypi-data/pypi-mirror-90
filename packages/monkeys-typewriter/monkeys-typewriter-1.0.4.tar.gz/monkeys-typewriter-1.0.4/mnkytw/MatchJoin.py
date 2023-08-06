# MatchJoin takes a list of matchers and joins them, to essentially
# make a conjunctive matcher
class MatchJoin:
    # @matchers A list of matchers to join into a single match for example
    # [
    #   LiteralMatch("hello ")
    #   LiteralMatch("world")
    # ]
    def __init__(self, matchers : list):
        self.to_string_call_count = None
        self.matchers = matchers

    # @body The body to parse and tokenise
    # @hard_fail a boolean flag indicating whether or not to throw an error when a match
    # doesn't work
    def parser(self, body : str, hard_fail = True):
        result = []
        head = 0
        for matcher in self.matchers:
            sub_body = body[head:]
            out = matcher.parser(sub_body, hard_fail = False)
            if not out:
                if hard_fail:
                    raise ValueError(f"MatchJoin: Could not match at {head}")
                else:
                    return False
            result.append(out[0])
            head += out[1]
        return (result, head)
    
    def to_string(self, call_count = 0):    
        if self.to_string_call_count == call_count:
            return "..."
        else:
            self.to_string_call_count = call_count
            return "(" + " ".join([m.to_string(call_count) for m in self.matchers]) + ")"

    def __str__(self):
        return self.to_string()
