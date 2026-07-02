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
    df['Tenure_Days'] = (pd.Timestamp.now() - df["Dt_Customer"]).dt.days
    df['TotalSpend'] = df.filter(like='Mnt').sum(axis=1)
    df['TotalPurchase'] = df[["NumWebPurchases", "NumCatalogPurchases", "NumStorePurchases"]].sum(axis=1)
    df['DealsProportion'] = df['NumDealsPurchases']/ df['TotalPurchase']
    df['Spend/purchase'] = df['TotalSpend']/ df["TotalPurchase"]
    df['HasChild'] = df[['Kidhome','Teenhome']].sum(axis=1)
    df['TotalCampaignAccept'] = df.filter(like='AcceptedCmp').sum(axis=1)
    return df

def rfm(df):
    #Recency: lower days = better = higher score (reverse)
    df["R_Score"] = pd.qcut(df["Recency"], q=5, labels=[5,4,3,2,1]).astype(int)
    #Frequency: more purchases = better = higher score
    df["F_Score"] = pd.qcut(df["TotalPurchase"].rank(method="first"), q=5, labels=[1,2,3,4,5]).astype(int)
    #Monetary: more spend = better = higher score 
    df["M_Score"] = pd.qcut(df["TotalSpend"].rank(method="first"), q=5, labels=[1,2,3,4,5]).astype(int)
    df["RFM_Score"] = df["R_Score"] + df["F_Score"] + df["M_Score"]

    def segment(score):
        if score >= 13: return "veryLoyal"
        elif score >= 10: return "Loyal"
        elif score >= 7: return "AtRisk"
        else: return "Lost"

    df["RFM_Segment"] = df["RFM_Score"].apply(segment)
    return df