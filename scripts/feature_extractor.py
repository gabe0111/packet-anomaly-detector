import pandas as pd

def extract_features(path="data/processed_packets.csv"):
    df = pd.read_csv(path)

    df["protocol"] = df["protocol"].fillna(0)
    df["flags"] = df["flags"].fillna("")

    df["flags_len"] = df["flags"].apply(len)
    df = df.drop(columns=["timestamp", "src_ip", "dst_ip", "flags"])

    return df
