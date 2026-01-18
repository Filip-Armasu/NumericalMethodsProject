import numpy as np
import matplotlib.pyplot as plt
from model import MarketModel
from plots import plot_market_share_bar

print("Starting Market Simulation...")

def run_simulation(steps=300): # Simulation parameters
    m = MarketModel(
        N_firms=15,
        N_consumers=100, 
        fixed_cost=90,  
        income_per_step=60,
        penalty_threshold=5,
        shareholder_penalty=3500,
        bonus_threshold=7,
        investor_bonus=10000,
        preference_modifier=0,
    )

    for _ in range(steps): 
        m.step()

    model_df = m.datacollector.get_model_vars_dataframe()
    agent_df = m.datacollector.get_agent_vars_dataframe()

    return m, model_df, agent_df 

if __name__ == "__main__": 
    m, model_df, agent_df = run_simulation(steps=300)
    print("Simulation completed.")
    plot_market_share_bar(model_df, m) # Plot market share bar chart