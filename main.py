import numpy as np
import matplotlib.pyplot as plt
from model import MarketModel
from plots import plot_market_share_bar

print("Starting Market Simulation...")

# Simulation parameters
def run_simulation(steps=300): # Number of steps in the simulation
    m = MarketModel(
        N_firms=20, # Number of firms in the market
        N_consumers=100,  # Number of consumers in the market
        fixed_cost=55,  # Fixed cost per step for each firm
        income_per_step=70, # Income each consumer provides per step
        penalty_threshold=6, # Loss streak required for penalty
        shareholder_penalty=5000, # Penalty for low performance
        bonus_threshold=2, # Win streak required for bonus
        investor_bonus=700, # Bonus for high performance
        brand_gain=0.005, # How much brand value increases per sale
        brand_decay=0.01, # How much brand value decays each step
        brand_weight=0.005, # How impactful the brand value is
        start_boost=100, # How much starting sales impact the simulation long term
        max_steps=steps
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