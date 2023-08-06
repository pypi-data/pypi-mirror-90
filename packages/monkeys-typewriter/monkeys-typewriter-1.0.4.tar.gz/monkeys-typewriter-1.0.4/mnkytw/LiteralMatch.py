# LiteralMatch does what it says on the tin, takes a literal such as "hello" and 
# matches it an only it. This is one of two axiomatic building blocks for a PEG parser.
# The other is RegexMatch
class LiteralMatch:
    
    # @val The value of to match to, can be any arbitrary string
    # Note that this function is case sensitive
    def __init__(self, val : str):
        self.expression = val

    # @body The body we are matching tokens to in parsing
    # @hard_fail A boolean flag indicating if a matcher should throw an error (or just return false)
    # This method parses a body of text for tokens
    def parser(self, body : str, hard_fail = True):
        #if the start of the body, to length of the expression to match
        # is the same as the expression to match then
        match = body[0:len(self.expression)] == self.expression
        #if not a match
        if not match:
            #If set to hard fail
            if hard_fail:
                #throw an error
                raise ValueError(f"LiteralMatch: Could not match '{self.expression}'")
            else:
                #else return false
                return False
        #if matched
        #return the expression and the length of the head as a tuple pair
        return (self.expression, len(self.expression))

    # @call_count A nonce used to detect recursion
    def to_string(self, call_count = 0):
        return f'"{self.expression}"'

    def __str__(self):
        return self.to_string()