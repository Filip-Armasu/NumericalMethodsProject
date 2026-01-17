import numpy as np
import matplotlib.pyplot as plt
from model import MarketModel
from plots import plot_market_share_bar

print("Starting Market Simulation...")

def run_simulation(steps=300):
    m = MarketModel(
        N_firms=20,
        N_consumers=200, 
        fixed_cost=20,  
        income_per_step=50
    )

    for _ in range(steps):
        m.step()

    model_df = m.datacollector.get_model_vars_dataframe()
    agent_df = m.datacollector.get_agent_vars_dataframe()

    return m, model_df, agent_df

if __name__ == "__main__":
    m, model_df, agent_df = run_simulation(steps=300)
    print("Simulation completed.")
    plot_market_share_bar(model_df, m)