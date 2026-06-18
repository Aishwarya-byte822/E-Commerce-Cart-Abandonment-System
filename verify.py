import pandas as pd
from sqlalchemy import create_engine
engine=create_engine("sqlite:///ecommerce.db")
df=pd.read_sql("SELECT COUNT(*) AS total_rows FROM events",engine)
print(df)
