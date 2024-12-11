import numpy as np
import pandas as pd

def read_input(fn):
    df = pd.read_csv(fn, header=None, sep="   ", index_col=False)
    df.columns = ["Group1", "Group2"]
    g1 = df["Group1"].astype(int).sort_values(ascending=True).values
    g2 = df["Group2"].astype(int).sort_values(ascending=True).values

    return pd.DataFrame({
        "Group1": g1,
        "Group2": g2
    })


def main(fn):
    df = read_input(fn)
    df["Group1"] = df["Group1"].sort_values(ascending=True)
    df["Group2"] = df["Group2"].sort_values(ascending=True)
    df["Distance"] = np.abs(df["Group2"] - df["Group1"])
    print(df["Distance"].sum())



if __name__ == "__main__":
    main("day1-input.txt")