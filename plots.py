import matplotlib.pyplot as plt
import numpy as np

def plot_market_share_bar(model_df, model):
    final_shares_alive = model_df["Shares"].iloc[-1]
    all_ids=[f.unique_id for f in model.firms]
    alive_ids=[f.unique_id for f in model.firms if f.alive]
    share_map = dict(zip(alive_ids, final_shares_alive))
    full_shares = [share_map.get(fid, 0.0) for fid in all_ids]

    plt.figure()
    plt.bar(all_ids, full_shares)
    plt.xlabel("Firm ID")
    plt.ylabel("Market Share")
    plt.title("Final Market Shares of Firms")
    plt.ylim(0, 1)
    plt.xticks(all_ids)
    plt.show()
