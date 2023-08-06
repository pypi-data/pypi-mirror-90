import examples.hello
import examples.maths

import mnkytw

matchNoMoreThanFive3s = mnkytw.MatchQuantity(
    mnkytw.LiteralMatch("3"),
    0, #Can match no threes
    5 # match at most 5 threes
)

print(matchNoMoreThanFive3s.parser("33", False))
# (['3', '3'], 2)

print(matchNoMoreThanFive3s.parser("333333", False))
# (['3', '3', '3', '3', '3'], 5)

print(matchNoMoreThanFive3s.parser("343", False))
# (['3'], 1)

print(matchNoMoreThanFive3s.parser("245", False))
# ([], 0)