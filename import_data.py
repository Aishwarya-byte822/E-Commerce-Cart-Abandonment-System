import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///ecommerce.db")

df = pd.read_csv("2019-Nov.csv",nrows=100000)
df.to_sql("events",engine,if_exists="replace",index=False)
print("Data is imported")


