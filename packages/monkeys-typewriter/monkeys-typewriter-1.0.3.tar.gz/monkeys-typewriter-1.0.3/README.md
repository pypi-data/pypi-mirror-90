# Monkey's Typewriter (mnkytw)

![logo](/images/mnkytw_logo.png)

Monkey's Typewriter is a PEG parsing framework for Python designed for simplicity, ease of understanding and liberal intepretation of PEG expression grammars. It is zero dependency and uses python's internal `re` regex library for matching axiomatic elements and then 3 complex matchers to allow you to express your grammars

## Pros and Cons

- Pro: The entire library is 6 files (ignoring examples and module files), and consists of only 6 classes and two functions to make writing easy
- Pro: You can write the grammars in an object oriented way, declaring your own custom matcher classes, allowing you spread your parser across multiple files, and unit test individual smaller matchers
- Con: This library does not perfectly conform to PEG parsing standards, for example, left recursion can be made to work using custom matchers
- Con: This library does not have complex quantification expressions, in-built zero-consumption negative lookahead expressions etc. They're fairly easily implementable, but not available as standard
- Con: No in-built whitespace handling. If you can think of an elegant way to do it that doesn't add too much overhead to the library, post a suggestion in the issues.
- Con (maybe Pro): A custom matcher can accidentally (or intentionally) backtrack if it chooses too, this can result in unexpected behaviour though because by default our classes assume no backtracking


## Getting Started
Monkey's Typewriter is a framework, because you have to build your own custom Matcher classes to achieve complex and custom parsing tress. Lets take a look at a simple example to begin with. We will build a parser that can parse expressions such as `3+4+5` giving us a tree where `lhs = 3, symbol = "+", rhs = { lhs = 4, symbol = "+", rhs = 5}`

This framework is similar to PEG.js in that you can customise the tokens we return for matches, meaning you can achieve a much more informative tree, more quickly and easily by configuring tokens as they're parsed

Let's begin by defining an Integer Matcher, we could write

```python
import mnkytw
Integer = mnkytw.MatchAlternation([
    mnkytw.RegexMatch(r"[1-9][0-9]*"),
    mnkytw.LiteralMatch("0")
])

mnkytw.parse("42", Integer)
```

However, when this is parsed, what we'll get back is the string `"42"` which, I mean sure it's a basic parser, but it doesn't really achieve anything. Instead lets cast it, and create a dict object for it to identify the token type

Instead of just using our existing match classes, we'll wrap it in it's own match class and implement some custom parsing logic

```python
import mnkytw

class IntegerMatch:
    def __init__(self):
        self.matcher = mnkytw.MatchAlternation([
            mnkytw.RegexMatch(r"[1-9][0-9]*"),
            mnkytw.LiteralMatch("0")
        ])

    def parser(self, body : str, hard_fail = True):
        # call the matcher
        result = self.matcher.parser(body, hard_fail)
        # if there's no result
        if not result:
            # just return it because it's a false value
            return result
        #if it does have a result though
        return [{
            #cast the match to an integer
            'val': int(result[0]),
            #add some extra sugar like a type and the type name
            'type': 'integer'
        }, result[1]] # always return the cursor position, otherwise you'll get backtracking

    #We should provide to_string and __str__ methods if we want to print our matchers
    def to_string(self, call_count = 0):
        return self.matcher.to_string(call_count)
    
    def __str__(self):
        return self.to_string()

Integer = IntegerMatch()

print(mnkytw.peg_parse("23", Integer))
# {
#   'val': '23',
#   'type': 'integer'
# }
```

A lot is going on above, but it's still fairly straight-forward. Firstly we create a class, and set `self.matcher` to the integer matcher we previously wrote. We then write a custom `parser` function that calls the matcher we just declared, but takes the tokenised result of that match, and casts it to an integer and then passes it up to the caller

What this essentially is a glorified function curry, where we build a faux-matcher that sits between the matcher we built using our base classes, and the `peg_parse` function provided by `mnkytw`.

You'll notice that we have to declare two string conversion functions. Because you can declare recursive matchers, when you string cast a matcher, it's possible for the string cast function to get stuck in an infinite loop. To prevent this you should use `mnkytw.to_string(matcher)` to convert a matcher to string, it will mark any second level recursions with a `...` to imply recursion

Finally, we want to declare a recursive matcher that can parse something like `"3+4+5"`.

Let's begin by defining the set of operator symbols that are valid

```python
import mnkytw

Operators = mnkytw.MatchAlternation([
    mnkytw.LiteralMatch("+"),
    mnkytw.LiteralMatch("-"),
    mnkytw.LiteralMatch("*"),
    mnkytw.LiteralMatch("/")
])

```

We don't need to define a custom class here, because all we really want is the symbol, there's no need to intercept parsing that we don't want to modify the token result of

Now lets declare a recursive matcher called OperationMatch

```python
import mnkytw

class OperationMatch:
    def __init__(self):
        # Match either
        self.matcher = mnkytw.MatchAlternation([
            mnkytw.MatchJoin([
                # An integer
                Integer,
                # followed by a symbol
                Operators,
                # followed by this matcher
                self
            ]),
            # or an integer
            Integer
        ])
    
    def parser(self, body : str, hard_fail = True):
        result = self.matcher.parser(body, hard_fail)
        if not result:
            return result
        # if the token matched was not a list, then it can't be
        # the MatchJoin that was matched (because a MatchJoin is always a list)
        if type(result[0]) is not list:
            # The only alternative is that it matched the Integer alternative so 
            # just pass that token up as is
            return result
        return [{
            'lhs': result[0][0], # the first part of the list will be the integer matched
            'symbol': result[0][1], # the second part matched will be a list
            'rhs': result[0][2] # the third part will be the tail recursion, it could be an
            #integer or another Operation but either way it doesn't matter because it's still the RHS
        }, result[1]]

    def to_string(self, call_count = 0):
        return self.matcher.to_string(call_count)
    
    def __str__(self):
        return self.to_string()

Operation = OperationMatch()

print(mnkytw.peg_parse("3+4", Operation))
# {
#   'lhs': {
#       'val': 3,
#       'type': 'integer'
#   },
#   symbol: '+',
#   'rhs': {
#       'val': 4,
#       'type': 'integer'
#   }
# }
```

In the example above, we use a little more logic in how we parse tokens, this time we're using what the token returned is to decide if further processing is required. In this case we know that the only circumstance in which the token returned is a list is if it's found a symbol in the middle. The return type of base classes can be found in the documentation

For this reason you should try to keep your grammar as decomposed as possible, to avoid the risk of making false assumptions about the typing of your more complex token result. 

## Reference

### `mnkytw.LiteralMatch`

The `LiteralMatch` class matches a string, and nothing else. A `LiteralMatch` takes a string as it's only constructor argument then attempts to match that when `parser` is called

```python
import mnkytw

Hello = mnkytw.LiteralMatch("hello")

print(Hello.parser("hello", False))
# ("hello", 5)
print(Hello.parser("goodbye", False))
# False
print(Hello.parser("hello hello", False))
# ("hello", 5)
# it ignores the second hello, it greedy matches but does not fail if it doesn't fully match
print(Hello.parser("goodbye", True))
# throws a ValueError

print(mnkyt.peg_parse("hello hello", Hello))
# False 
# because peg_parse expects a complete match to the string, not just a start anchored substring

```

### `mnkytw.RegexMatch`

The `RegexMatch` class matches a regex. A `RegexMatch` takes a Regex string as it's only constructor argument then uses this when parsing the text body. Because this is just a wrapper around Python's Regex Library, it's possible to implement some backtracking and various other complex matching patterns. 

This isn't recommended, because the more complex Regex you define, the harder you make it to debug. You should focus on making your Regex declaration axiomatic (i.e. matching only one axiomatic element). In certain cases, it may be more readable to use a `MatchAlternation` and a set of `LiteralMatch` declarations to express the pattern you're aiming to match.

```python
import mnkytw

FloatingPoint = mnkytw.RegexMatch(r"[0-9]+\.[0-9]*[1-9]")

print(FloatingPoint.parser("3.141", False))
# ('3.141', 5)
```

### `mnkytw.MatchAlternation`

The `MatchAlternation` class is the Monkey's Typewriter disjunction. That is to say, it will attempt to match one of the listed matches starting at the top of the list and working down e.g.

```python
import mnkytw
MatchFewest1s = mnkytw.MatchAlternation([
    mnkytw.LiteralMatch("1"), # this literal will be matched first
    mnkytw.LiteralMatch("11"), # this match will be matched second
    mnkytw.LiteralMatch("111"), # this will be matched third
    mnkytw.RegexMatch(r"1*"), # this will be matched last
])

print(MatchFewest1s.parser("111111", False))
# ('1', 1)

```

In the example above, because `"1"` matched first, it matched that and returned. Even though the last RegexMatch would have matched the most of the string (i.e. all of it), the MatchAlternation will take the first positive match in the list.

As a result, your alternations should be setup with this in mind e.g.

```python
import mnkytw
MatchAsMany1sUpToThree = mnkytw.MatchAlternation([
    mnkytw.LiteralMatch("111"), # this will be matched first
    mnkytw.LiteralMatch("11"), # this match will be matched second
    mnkytw.LiteralMatch("1"), # this literal will be matched third
])

print(MatchAsMany1sUpToThree.parser("111111", False))
# ('111', 3)

```

Now that we've re-ordered our `MatchAlternation` list, it's testing the three `1`s first and so consuming that.

### `mnkytw.MatchJoin`
The `MatchJoin` is Monkey's Typewriter's Conjunction class. Essentially, it forces multiple matchers to join together. This can be used to express more complex expressions composed of multiple matchers.

```python
import mnkytw

twoOrThree = mnkytw.MatchAlternation([
    mnkytw.LiteralMatch("2"),
    mnkytw.LiteralMatch("3"),
])
fourOrFive = mnkytw.MatchAlternation([
    mnkytw.LiteralMatch("4"),
    mnkytw.LiteralMatch("5"),
])

twoOrThreeAndFourOrFive = mnkytw.MatchJoin([
    twoOrThree,
    fourOrFive
])

print(twoOrThreeAndFourOrFive.parser("24", False))
# (['2', '4'], 2)
print(twoOrThreeAndFourOrFive.parser("34", False))
# (['3', '4'], 2)
print(twoOrThreeAndFourOrFive.parser("356", False))
# (['3', '5'], 2)

print(twoOrThreeAndFourOrFive.parser("156", False))
# False

```

A `MatchJoin` returns a list of the tokens it matched, in the case above, we provided two matchers, and it matched each once, except in the last example, because the first digit was a `1` not a `2` or `3`. 

Note, that if you write a custom Matcher you return result may also be a list. Whilst none of the library logic makes the assumption that only `MatchJoin` (and `MatchQuantity`) return lists, we do use it in some of our examples. If you return a list as your token, then you will need to work out an alternative way of distinguishing the result of a `MatchJoin` from your own custom matchers.

### `mnkytw.MatchQuantity`

The `MatchQuantity` class is our quantified match class. essentially, allowing you specify a minimum (and optional maximum) number of times a given matcher should be matched. The `MatchQuantity` class returns a list of tokens matched.

```python
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

```

This class can act as an optional match class and "+" match class simply by writing `mnkytw.MatchQuantity(your_matcher, 0, 1)` `mnkytw.MatchQuantity(your_matcher, 1)`. The maximum value is optional and if unset we will assume you want to match until first failure or end of input.