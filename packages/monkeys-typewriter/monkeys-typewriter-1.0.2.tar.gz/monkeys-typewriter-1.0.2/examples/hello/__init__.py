import mnkytw

# Declare a basic literal matcher
Hello = mnkytw.LiteralMatch("Hello ")

class MultipleHellosMatch:
    # In the class initialised
    def __init__(self):
        # declare your compound matcher
        self.matcher = mnkytw.MatchAlternation([
            mnkytw.MatchJoin([
                Hello,
                # With recursion
                self,
            ]),
            Hello,
        ])

    # Declare your parser function, and return a result
    def parser(self, body : str, hard_fail = True):
        result = self.matcher.parser(body, hard_fail)
        return result

    def to_string(self, call_count = 0):
        return self.matcher.to_string(call_count)
    
    def __str__(self):
        return self.to_string()

MultipleHellos = MultipleHellosMatch()

#parse the string "Hello Hello Hello"
print(
    mnkytw.peg_parse("Hello Hello Hello ", MultipleHellos)
)

#parse the single string "Hello "
print(
    mnkytw.peg_parse("Hello ", MultipleHellos)
)

#print the grammar as a PEG.js style grammar (ish)
print(mnkytw.to_string(MultipleHellos))
