import numpy as np
import mesa
from mesa.datacollection import DataCollector
import random
import matplotlib.pyplot as plt
import pandas as pd

class Firm(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.product_type = random.choice(["electronics", "clothing", "food"])
        self.capital = random.randint(5000, 10000)
        self.production_cost = random.randint(5, 20)
        self.price = self.production_cost + random.randint(1, 10)

class Consumer(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = random.randint(1000, 5000)
        self.preference = random.choice(["electronics", "clothing", "food"])
        self.budget = random.randint(self.wealth//10, self.wealth)

    def step(self):
        firm = self.random.choice(self.model.firms)
        if self.budget >= firm.price:
            if self.preference == firm.product_type:
                self.budget += 250  # Increase budget if preference matches
            else:
                self.budget -= 100  # Decrease budget if preference does not match
            self.wealth -= firm.price
            firm.capital += firm.price

