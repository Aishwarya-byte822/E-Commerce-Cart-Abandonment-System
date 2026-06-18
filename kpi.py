import pandas as pd
from sqlalchemy import create_engine

engine=create_engine("sqlite:///ecommerce.db")
df=pd.read_sql("""SELECT COUNT(DISTINCT user_id) as total_users
               FROM events""",engine)
print(df)
