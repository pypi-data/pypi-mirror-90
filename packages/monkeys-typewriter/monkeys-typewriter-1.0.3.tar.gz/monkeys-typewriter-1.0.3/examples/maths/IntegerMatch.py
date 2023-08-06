import mnkytw
class IntegerMatch:
    def __init__(self):
        #Match either
        self.matcher = mnkytw.MatchAlternation([
            #A 1 to 9 followed by any number of digits
            mnkytw.RegexMatch(r"[1-9][0-9]*"),
            #or a zero
            mnkytw.LiteralMatch("0")
        ])

    def parser(self, body : str, hard_fail = True):
        #Attempt to match to the matcher
        result = self.matcher.parser(body, hard_fail)
        # if it's not a match, and we're here, we can assume that
        # we haven't been told to "hard fail", so just return the false
        # result
        if not result:
            return result
        
        # Return your own token result, but the second value must always
        # be the cursor position within the body, so make sure you always return
        # result[1] as the second argument
        return [{
            'val': int(result[0]),
            'type': 'integer'
        }, result[1]]

    def to_string(self, call_count = 0):
        return self.matcher.to_string(call_count)

    def __str__(self):
        return self.to_string()