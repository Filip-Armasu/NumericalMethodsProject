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
def animate_market(
    steps=100,
    interval=0.01,
    N_firms=15,
    N_consumers=200, 
    fixed_cost=50,  
    income_per_step=75,
    penalty_threshold=8,
    shareholder_penalty=1000,
    bonus_threshold=5,
    investor_bonus=1500,
    brand_gain=0.001,
    brand_decay=0.03,
    brand_weight=0.03,   
):
    model = MarketModel(
        N_firms=N_firms,
        N_consumers=N_consumers,
        fixed_cost=fixed_cost,
        income_per_step=income_per_step,
        penalty_threshold=penalty_threshold,
        shareholder_penalty=shareholder_penalty,
        bonus_threshold=bonus_threshold,
        investor_bonus=investor_bonus,
        brand_gain=brand_gain,
        brand_decay=brand_decay,
        brand_weight=brand_weight,
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