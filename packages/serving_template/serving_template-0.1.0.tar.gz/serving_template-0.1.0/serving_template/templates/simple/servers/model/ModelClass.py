import random


class ModelClass:
    def __init__(self):
        pass

    def predict(self, inputs):
        return [random.random() for x in inputs]
