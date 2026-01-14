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

class MarketModel(mesa.Model):
    def __init__(self, N_firms, N_consumers):
        super().__init__()
        self.num_firms = N_firms
        self.num_consumers = N_consumers

        self.firms = [Firm(i, self) for i in range(self.num_firms)]
        self.consumers = [Consumer(i + self.num_firms, self) for i in range(self.num_consumers)]

        self.schedule = mesa.time.RandomActivation(self)
        for firm in self.firms:
            self.schedule.add(firm)
        for consumer in self.consumers:
            self.schedule.add(consumer)

        self.datacollector = DataCollector(
            model_reporters={
                "Total_Market": self.total_market,
                "Market_Share": self.market_share
            }
        )

    def total_market(self):
        total = 0
        for consumer in self.consumers:
            for firm in self.firms:
                if consumer.budget >= firm.price:
                    total += firm.price
        return total
    
    def market_share(self):
        share = {}
        total_sales = self.total_market()
        for firm in self.firms:
            firm_sales = sum(firm.price for consumer in self.consumers if consumer.budget >= firm.price)
            share[firm.unique_id] = firm_sales / total_sales if total_sales > 0 else 0
        return share

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
