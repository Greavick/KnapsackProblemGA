import random


# Class representing single item.
# Holds weight of an item and it's value.

class Item:
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight

    def __repr__(self):
        return "(" + str(self.value) + ", " + str(self.weight) + ")"


# Class representing knapsack.

class Knapsack:

    # Constructor randomly assigns whether items are packed or not.

    def __init__(self, items):
        self.packed = []
        self.fitness = 0
        self.items = items
        self.number_of_items = len(items)
        for i in range(self.number_of_items):
            r = random.random()
            self.packed.append(True if r > 0.5 else False)

    # Evaluation process result in the sum of values in case the knapsack if weights remains within threshold
    # otherwise fitness is set to negated value of the sum of weights

    def evaluate(self, threshold):
        weight = 0
        value = 0
        for i in range(len(self.packed)):
            if self.packed[i]:
                weight += self.items[i].weight
                value += self.items[i].value

        if weight <= threshold:
            self.fitness = value
        else:
            self.fitness = -weight

        return self.fitness

    def __repr__(self):
        return str([1 if i else 0 for i in self.packed])
