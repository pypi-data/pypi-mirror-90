import mnkytw
class FloatMatch:
    def __init__(self):
        # A float is at least one digit before a decimal point
        # followed by any number of zero inclusive digits, and
        # finally a digit between 1 and 9
        self.matcher = mnkytw.RegexMatch(r"[0-9]+\.[0-9]*[1-9]")

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
            'val': float(result[0]),
            'type': 'float'
        }, result[1]]

    def to_string(self, call_count = 0):
        return self.matcher.to_string(call_count)

    def __str__(self):
        return self.to_string()