# test_pipeline.py
import pandas as pd
from pipeline.data_processor import *

df = pd.read_csv("data/marketing_campaign.csv", sep=";")
df = feat_engine(df)
print(df['age'])