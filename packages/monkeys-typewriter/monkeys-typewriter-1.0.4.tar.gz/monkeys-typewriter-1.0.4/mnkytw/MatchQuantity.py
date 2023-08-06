class MatchQuantity:
    def __init__(self, matcher, min_n = 0, max_n = -1):
        self.matcher = matcher
        self.min = min_n
        self.max = max_n

    def parser(self, body : str, hard_fail = True):
        head = 0
        count = 0
        result = []
        while True:
            sub_body = body[head:]
            # If max is specified and we've reached it
            if self.max > 0 and self.max == count:
                # return the result and the head
                return (result, head)
            match = self.matcher.parser(sub_body, hard_fail = False)
            if not match or head == len(body):
                break
            head += match[1]
            result.append(match[0])
            count += 1
        
        if count < self.min:
            if hard_fail:
                raise ValueError(f"MatchQuantity: less than minimum matches")
            else:
                return False
        
        return (result, head)

    def to_string(self, call_count = 0):
        return f"({self.matcher.to_string(call_count)}){{{self.min},{self.max}}}"

    def __str__(self):
        return self.to_string()