import matplotlib.pyplot as plt
import numpy as np
import random

def plot_market_share_bar(model_df, model): # Bar chart of market shares
    final_shares_alive = model_df["Shares"].iloc[-1]
    all_ids=[f.unique_id for f in model.firms]
    alive_ids=[f.unique_id for f in model.firms if f.alive] # Only alive firms
    share_map = dict(zip(alive_ids, final_shares_alive))
    full_shares = [share_map.get(fid, 0.0) for fid in all_ids]

    # Random Colors
    colors = [(
    random.random(),
    random.random(),
    random.random(),
    ) for _ in all_ids]

    # Plotting the bar chart
    fig, ax = plt.subplots()
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle() # Making it full screen so it looks good on video
    bars = ax.bar(all_ids, full_shares, color=colors) # Making each bar a different color
    ax.set_xlabel("Firm ID")
    ax.set_ylabel("Market Share")
    ax.set_title("Final Market Shares of Firms")
    ax.set_ylim(0, 1)
    ax.set_xticks(all_ids)

    # Showing percentage labels on top of bars
    for bar, share in zip(bars, full_shares):
        if share > 0:
            ax.text(
            bar.get_x() + bar.get_width() / 2,
            share,
            f"{share * 100:.1f}%",
            ha="center",
            va="bottom",
            fontsize=9
    )
            
    plt.show()
    
