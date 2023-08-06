import re

class RegexMatch:
    def __init__(self, reg : str):
        #We store the regex to make printing easier
        self.expression = reg
        #compile it into an actual regex though
        self.regexr = re.compile(reg)

    def parser(self, body : str, hard_fail = True):
        #match the body, to the regex 
        # (we use match because we're essentially start anchoring)
        match = self.regexr.match(body)
        # if not a match
        if not match:
            # if hard fail is true
            if hard_fail:
                # throw an error
                raise ValueError(f"RegexMatch: Could not match '{self.expression}'")
            else:
                #otherwise just return false
                return False
        #return the match and the head of the string (i.e. where in the body we are now)
        return (match.group(0), match.span()[1])

    def to_string(self, call_count = 0):
        return f'"{self.expression}"'

    def __str__(self):
        return self.to_string()