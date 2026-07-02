# test_pipeline.py
import pandas as pd
from pipeline.data_processor import *

df = pd.read_csv("data/marketing_campaign.csv", sep=";")
df = clean(df)
df = feat_engine(df)
df = rfm(df)
print(df.iloc[:,-5:])