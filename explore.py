import pandas as pd
from sqlalchemy import create_engine
engine = create_engine("sqlite:///ecommerce.db")
df=pd.read_sql("""SELECT event_type,COUNT(*) as total
               FROM events
               GROUP BY event_type""", engine)
print(df)

