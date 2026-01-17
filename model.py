import numpy as np
import mesa
from mesa.time import RandomActivation
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

        self.units_sold = 0
        self.revenue = 0.0
        self.cumulative_revenue = 0.0
        self.profit = 0.0
        self.alive = True

    def reset_step_stats(self):
        self.units_sold = 0
        self.revenue = 0.0
        self.profit = 0.0

    def record_sale(self, units: int = 1):
        self.units_sold += units
        self.revenue += units * self.price
        self.cumulative_revenue += units * self.price

    def finalize_profit(self):
        self.profit = self.revenue - (self.units_sold * self.production_cost)- self.model.fixed_cost
        self.capital += self.profit

        if self.capital <= 0:
            self.alive = False

    def step(self):
        pass

class Consumer(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = random.randint(1000, 5000)
        self.preference = random.choice(["electronics", "clothing", "food"])
        self.budget = random.randint(self.wealth//10, self.wealth)

    def choose_firm(self, firms):
        affordable_firms = [firm for firm in firms if firm.price <= self.budget]
        if not affordable_firms:
            return None
        preferred_firms = [firm for firm in affordable_firms if firm.product_type == self.preference]
        if preferred_firms:
            return self.random.choice(preferred_firms)
        return self.random.choice(affordable_firms)

    def step(self):
        firms = [f for f in self.model.firms if f.alive]
        if not firms:
            return
    
        firm = self.choose_firm(firms)
        if firm is None:
            self.budget += self.model.income_per_step  # Increase budget if no affordable firms
            return
        
        if self.budget >= firm.price:
            self.budget -= firm.price
            self.wealth -= firm.price
            firm.record_sale(1)

            if self.preference == firm.product_type:
                self.budget += 250  # Increase budget if preference matches
            else:
                self.budget = max(0, self.budget - 100)  # Decrease budget if preference does not match
        else:
            self.budget += self.model.income_per_step  # Increase budget if cannot afford

class MarketModel(mesa.Model):
    def __init__(self, N_firms, N_consumers, fixed_cost=20, income_per_step=50):
        super().__init__()
        self.num_firms = N_firms
        self.num_consumers = N_consumers
        self.fixed_cost = fixed_cost
        self.income_per_step = income_per_step
        self.raise_price_threshold = 5

        self.firms = [Firm(i, self) for i in range(self.num_firms)]
        self.consumers = [Consumer(i + self.num_firms, self) for i in range(self.num_consumers)]

        self.schedule = RandomActivation(self)
        for consumer in self.consumers:
            self.schedule.add(consumer)

        self.datacollector = DataCollector(
            model_reporters={
                "Total_Revenue": self.total_revenue,
                "Active_Firms": self.active_firms,
                "HHI": self.hhi,
                "Top_Share": self.top_share,
                "Shares": self.market_shares,
            },
            agent_reporters={
                "capital": lambda a: getattr(a, "capital", None),
                "price": lambda a: getattr(a, "price", None),
                "alive": lambda a: getattr(a, "alive", None),
            }
        )

    def active_firms(self):
        return sum(1 for firm in self.firms if firm.alive)
    
    def total_revenue(self):
        return sum(firm.revenue for firm in self.firms if firm.alive)
    
    def cumulative_revenue_function(self):
        return sum(firm.cumulative_revenue for firm in self.firms if firm.alive)
    
    def market_shares(self):
        total = self.cumulative_revenue_function()
        if total <= 0:
            return [0.0 for _ in self.firms]
        return [(firm.cumulative_revenue / total) if firm.alive else 0.0 for firm in self.firms]
    
    def hhi(self):
        shares = self.market_shares()
        return sum(share ** 2 for share in shares) * 10000  # HHI scaled by 10,000

    def top_share(self):
        shares = self.market_shares()
        if not shares:
            return 0.0
        return max(shares)

    def step(self):
        #reset stats for firms
        for firm in self.firms:
            firm.reset_step_stats()

        # Step all agents
        self.schedule.step()

        # Adjust prices based on sales
        for firm in self.firms:
            if not firm.alive:
                continue

            if firm.units_sold == 0:
                firm.price = max(firm.production_cost + 1, firm.price - 1)
            elif firm.units_sold > self.raise_price_threshold:
                firm.price += 1
            # Adjust price based on capital
            if firm.capital > 15000:
                firm.price += 1
            elif firm.capital < 7000:
                firm.price = max(firm.production_cost + 1, firm.price - 1)

        # Finalize profits and check for exit
        for firm in self.firms:
            if firm.alive:
                firm.finalize_profit()

        #Collect data
        self.datacollector.collect(self)
        
