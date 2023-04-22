class Deque:

    def __init__(self, *args):
        self.deque = list(args)

    def append(self, *args):
        for arg in args:
            self.deque.append(arg)
        return

    def append_left(self, *args):
        # appending arguments in reverse on the right, holding first argument in temp
        # then sliding all values to the right, and first value <- temp.
        self.deque += [arg for arg in reversed(args)]
        for i in args:
            temp = self.deque[-1]
            for index, value in enumerate(self.deque[-1:0:-1]):
                index = len(self.deque) - index - 1
                self.deque[index] = self.deque[index - 1]
            self.deque[0] = temp

    def pop(self):
        if len(self.deque) == 0:
            raise ValueError('Dequeue is empty!')
        del self.deque[-1]

    def pop_left(self):
        if len(self.deque) == 0:
            raise ValueError('Dequeue is empty!')
        del self.deque[0]

    def count(self):
        return len(self.deque)

    def clear(self):
        self.deque = []


















