class TimeControl:
    def __init__(self, string_repr):
        if string_repr != "-":
            self.initial_seconds = int(string_repr.split("+")[0])
            self.increment_seconds = int(string_repr.split("+")[1])
            self.score = min(10, (self.increment_seconds + 40 * self.increment_seconds) / 180)
        else:
            self.score = 0