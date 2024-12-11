import numpy as np
import pandas as pd

def read_input(fn):
    df = pd.read_csv(fn, header=None, sep="   ", index_col=False)
    # print(df.head())
    # print(df.shape)
    df.columns = ["Group1", "Group2"]
    g1 = df["Group1"].astype(int).sort_values(ascending=True).values
    g2 = df["Group2"].astype(int).sort_values(ascending=True).values

    return {
        "Group1": g1,
        "Group2": g2
    }


def main(fn):
    d = read_input(fn)

    g1_hist = np.bincount(d["Group1"])
    minlen = g1_hist.shape[0]
    g2_hist = np.bincount(d["Group2"], minlength=minlen)[:minlen]
    indexer = np.arange(minlen)

    print((indexer * g1_hist * g2_hist).sum())


if __name__ == "__main__":
    main("day1-input.txt")