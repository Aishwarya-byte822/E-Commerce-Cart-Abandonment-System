import pandas as pd
from sqlalchemy import create_engine
engine=create_engine("sqlite:///ecommerce.db")

df=pd.read_sql("""SELECT brand,COUNT(*) as purchases
               FROM events
               WHERE event_type='purchase'
               GROUP BY brand
               ORDER BY purchases DESC
               LIMIT 10""",engine)
print(df)
