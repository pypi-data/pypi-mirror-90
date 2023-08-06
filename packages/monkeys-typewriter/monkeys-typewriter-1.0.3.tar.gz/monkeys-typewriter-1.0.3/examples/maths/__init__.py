import mnkytw
from examples.maths.IntegerMatch import IntegerMatch
from examples.maths.FloatMatch import FloatMatch

# Create a single unified matcher that attempts to identify
# an integer or a float
Constants = mnkytw.MatchAlternation([
    FloatMatch(),
    IntegerMatch()
])

# symbols
Symbols = mnkytw.MatchAlternation([
    mnkytw.LiteralMatch("+"),
    mnkytw.LiteralMatch("-"),
    mnkytw.LiteralMatch("*"),
    mnkytw.LiteralMatch("/")
])

class OperationMatch:
    def __init__(self):
        self.matcher = mnkytw.MatchAlternation([
            # Either this is a chain of operations
            mnkytw.MatchJoin([
                Constants,
                Symbols,
                self
            ]),
            # Or a constant
            Constants
        ])
    
    def parser(self, body : str, hard_fail = True):
        result = self.matcher.parser(body, hard_fail)
        if not result:
            return result
        
        #we can infer that it matched the "MatchJoin" if it's a list
        if type(result[0]) is list:
            # make a dictionary that shows the lhs and rhs and the symbol
            return [{
                'lhs': result[0][0],
                'symbol': result[0][1],
                'rhs': result[0][2]
            }, result[1]]
        else:
            #Otherwise it matched the constant so just return the constant
            return result
        
Operation = OperationMatch()

print(mnkytw.peg_parse("3+4", Operation))

print(mnkytw.peg_parse("3+4+5", Operation))

print(mnkytw.peg_parse("3+4*5-6", Operation))