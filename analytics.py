import pandas as pd
from sqlalchemy import create_engine 
engine = create_engine("sqlite:///ecommerce.db")

users=pd.read_sql("""SELECT COUNT(DISTINCT user_id)as total_users
                  FROM events""",engine)

purchases=pd.read_sql("""SELECT COUNT(*) as total_purchases
                      FROM events
                      WHERE event_type='purchase'""",engine)

revenue=pd.read_sql("""SELECT ROUND(SUM(price),2) as revenue
                    FROM events
                    WHERE event_type='purchase'""", engine)

print("Total Users") 
print(users)

print("\nTotal Purchases")
print(purchases)

print("\nRevenue")
print(revenue)


