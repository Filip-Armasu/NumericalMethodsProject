import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import random
from model import MarketModel


def shares_all_firms(model): # Calculate market shares for all firms, alive or not
    total = sum(f.cumulative_revenue for f in model.firms if f.alive)
    if total <= 0:
        return [0.0 for _ in model.firms]

    return [(f.cumulative_revenue / total) if f.alive else 0.0 for f in model.firms] 

# Simulation parameters
def animate_market(steps=400, interval=0.0001,): # N8umber of steps and interval between frames
    model = MarketModel(
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
    
    firm_ids = [f.unique_id for f in model.firms] 

    # Random Colors
    colors = [(
    random.random(),
    random.random(),
    random.random(),
    ) for _ in firm_ids]

    # Set up the plot
    plt.ion()
    fig, ax = plt.subplots()
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle() # Making it full screen so it looks good on video
    bars = ax.bar(firm_ids, [0.0] * len(firm_ids), color=colors) # Making each bar a different color
    ax.set_ylim(0, 1)
    ax.yaxis.set_major_formatter(PercentFormatter(1.0))
    ax.set_xlabel("Firm ID")
    ax.set_ylabel("Market Share")
    title = ax.set_title("Market Shares (Step 0)")
    ax.set_xticks(firm_ids)

    # Showing percentage labels on top of bars
    labels = [
    ax.text(bar.get_x() + bar.get_width() / 2, 0, "",
    ha="center", va="bottom", fontsize=8)
    for bar in bars]
    
    # Animation loop
    for t in range(steps):
        model.step()

        shares = shares_all_firms(model)

        for bar, label, firm, h in zip(bars, labels, model.firms, shares):
            bar.set_height(h if firm.alive else 0.0)

            if firm.alive and h > 0:
                label.set_text(f"{h*100:.2f}%")
                label.set_y(h)
            else:
                label.set_text("")


        alive_count = sum(1 for f in model.firms if f.alive)
        title.set_text(f"Market Shares (Step {t+1}) | Active firms: {alive_count}")

        fig.canvas.draw_idle()
        plt.pause(interval)

    plt.ioff()
    plt.show() 


if __name__ == "__main__": 
    animate_market()