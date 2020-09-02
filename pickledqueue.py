class Queue:

    def __init__(self):
        self.queue = list()

    def add(self, item):
        if item not in self.queue:
            self.queue.insert(0, item)
            return True
        return False

    def check(self):
        while len(self.queue) > 5:
            self.queue.pop()