import matplotlib.pyplot as plt
import random

def plot_market_share_bar(model_df, model):

    all_ids = [f.unique_id for f in model.firms]

    final_shares_row = model_df["Shares"].iloc[-1] # Shares of the last step

    alive_ids = [f.unique_id for f in model.firms if f.alive]
    if len(final_shares_row) == len(alive_ids):
        share_map = dict(zip(alive_ids, final_shares_row))
    else:
        share_map = dict(zip(all_ids, final_shares_row))

    full_shares = [share_map.get(fid, 0.0) for fid in all_ids]

    total = sum(full_shares)
    if total > 0:
        full_shares = [s / total for s in full_shares]

    # Generate random colors
    colors = [(
    random.random(),
    random.random(), 
    random.random()
    ) for _ in all_ids]

    # Create figure
    fig, ax = plt.subplots()
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle() # Making it full screen so it looks good on video
    bars = ax.bar(range(len(all_ids)), full_shares, color=colors)

    # Labels and title
    ax.set_xlabel("Firm ID")
    ax.set_ylabel("Market Share")
    ax.set_title("Final Market Shares of Firms")
    ax.set_ylim(0, 1)
    ax.set_xticks(range(len(all_ids)))
    ax.set_xticklabels(all_ids)

    # Show percentage labels on top of bars
    for bar, share in zip(bars, full_shares):
        if share > 0:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                share + 0.01,
                f"{share * 100:.1f}%",
                ha="center",
                va="bottom",
                fontsize=9
            )

    plt.tight_layout()
    plt.show()
