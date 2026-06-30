import pandas as pd
from datetime import datetime

def clean(df):
    df = df.dropna(subset=["Income"])
    df["Dt_Customer"] = pd.to_datetime(df["Dt_Customer"])
    df = df[df["Year_Birth"] >= 1930]
    df = df[df["Income"] < 200000]
    return df

def feat_engine(df):
    df['age'] = datetime.now().year - df['Year_Birth']
    return df