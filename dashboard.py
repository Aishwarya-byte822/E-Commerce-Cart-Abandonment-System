import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

      # Page Configuration
st.set_page_config(
page_title="E-Commerce Dashboard",
page_icon="🛒",
layout="wide"
)
    
engine=create_engine("sqlite:///ecommerce.db")
      # Sidebar Filters
st.sidebar.title("Dashboard Filters")
brands_filter = pd.read_sql("""
            SELECT DISTINCT brand
            FROM events
            WHERE brand IS NOT NULL
            ORDER BY brand
            """, engine)

selected_brand = st.sidebar.selectbox(
"Select Brand",
["All"] + brands_filter["brand"].tolist()
)

categories_filter = pd.read_sql("""
            SELECT DISTINCT category_code
            FROM events
            WHERE category_code IS NOT NULL
            ORDER BY category_code
            """, engine)

selected_category = st.sidebar.selectbox(
"Select Category",
["All"] + categories_filter["category_code"].tolist()
)

selected_event = st.sidebar.selectbox(
"Select Event",
["All", "view", "cart", "purchase"]
)

st.info(
f"Selected Filters -> Brand: {selected_brand} | "
f"Category: {selected_category} | "
f"Event: {selected_event}"
)


safe_brand = selected_brand.replace("'", "''")
safe_category = selected_category.replace("'", "''")
 # Build conditional SQL WHERE clauses dynamically based on dropdown selections
if selected_brand == "All":
  brand_condition = ""
else:
  brand_condition = f"AND brand='{safe_brand}'"
if selected_category == "All":
  category_condition = ""
else:
  category_condition = f"AND category_code='{safe_category}'"
if selected_event == "All":
  event_condition = ""
else:
  event_condition = f"AND event_type='{selected_event}'"

# Main Dashboard Header Text
st.markdown("""E-Commerce Cart Abandonment Analytics
Track customer behavior, purchases,
revenue and cart abandonment trends.""")  

st.title("E-COMMERCE Analytics DASHBOARD")
st.success("Real E-Commerce Dataset Analysis")
st.caption("Built using Python, SQLAlchemy, SQLITE, Pandas and streamlit")


            # KPI Queries
users=pd.read_sql(f"""
                   SELECT COUNT(DISTINCT user_id) as total_users
                   FROM events
                   WHERE 1=1 
                  {brand_condition}
                  {category_condition}
                  {event_condition}
                  """, engine)

purchases_kpi=pd.read_sql(f"""
                      SELECT COUNT(*) as total_purchases
                      FROM events
                      WHERE event_type='purchase'
                      {brand_condition} 
                      {category_condition}
                      """,engine)

revenue=pd.read_sql(f"""SELECT ROUND(SUM(price),2) as revenue
                   FROM events
                   WHERE event_type='purchase'
                  {brand_condition}
                  {category_condition}
                  """,engine)
revenue_val = revenue.iloc[0,0] if pd.notnull(revenue.iloc[0,0]) else 0.0

# Count unique users who put items in a cart but never bought anything
abandoned=pd.read_sql(f"""SELECT COUNT(DISTINCT user_id) as abandoned_users
                   FROM events
                   WHERE event_type='cart'
                  {brand_condition}
                  {category_condition}
                   AND user_id NOT IN (
                    SELECT DISTINCT user_id
                    FROM events
                    WHERE event_type='purchase')""", engine)

st.subheader("📊 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Users", int(users.iloc[0,0]) if pd.notnull(users.iloc[0,0]) else 0 ) 
col2.metric("Purchases", int(purchases_kpi.iloc[0,0]) if pd.notnull(purchases_kpi.iloc[0,0]) else 0 )
col3.metric("Revenue", f"${revenue_val:,.2f}")
col4.metric("Abandoned Users", int(abandoned.iloc[0,0]) if pd.notnull(abandoned.iloc[0,0]) else 0)
st.divider()

# Visualizations & Data Tables Section
events=pd.read_sql(f"""SELECT event_type,
           COUNT(*) as total
           FROM events
            WHERE 1=1 {brand_condition} {category_condition}      
           GROUP BY event_type""",engine)
st.subheader("Event Distribution")
st.bar_chart(events.set_index("event_type"))
top_brands = pd.read_sql(f"""
            SELECT brand, COUNT(*) as purchases
            FROM events
            WHERE event_type='purchase'
            AND brand IS NOT NULL
            {brand_condition}
            {category_condition}
            GROUP BY brand
            ORDER BY purchases DESC
            LIMIT 10""", engine)

st.subheader("Top 10 Brands")
st.dataframe(top_brands)
st.bar_chart(top_brands.set_index("brand"))

brand_revenue=pd.read_sql(f"""
                 SELECT brand,ROUND(SUM(price), 2) as revenue
                 FROM events
                 WHERE event_type='purchase'
                 AND brand IS NOT NULL
                 {brand_condition}
                 {category_condition}
                 GROUP BY brand
                 ORDER BY revenue DESC
                 LIMIT 10""", engine)

st.subheader("Revenue by Brand")
st.dataframe(brand_revenue)
st.bar_chart(brand_revenue.set_index("brand"))

categories = pd.read_sql(f"""
                SELECT category_code, COUNT(*) as total
                FROM events
                WHERE category_code IS NOT NULL
                {brand_condition}
                {category_condition}
                GROUP BY category_code
                ORDER BY total DESC
                LIMIT 10""", engine)

st.subheader("Top Categories")
st.dataframe(categories)
st.bar_chart(categories.set_index("category_code"))

abandoned_brands = pd.read_sql(f"""SELECT brand,
                COUNT(*) as carts
                FROM events
                WHERE event_type='cart'
                AND brand IS NOT NULL
                {brand_condition}
                {category_condition}
                GROUP BY brand
                ORDER BY carts DESC
                LIMIT 10""", engine)

st.subheader("Most Abandoned Brands")
st.dataframe(abandoned_brands)
st.bar_chart(abandoned_brands.set_index("brand"))
  #  Event Distribution
views = pd.read_sql(f"""
         SELECT COUNT(*) as total
         FROM events
         WHERE event_type='view'
         {brand_condition}
         {category_condition}
         """, engine)

carts = pd.read_sql(f"""SELECT COUNT(*) as total
        FROM events
        WHERE event_type='cart'
        {brand_condition}
        {category_condition}""", engine)
purchases_count = pd.read_sql(f"""SELECT COUNT(*) as total
        FROM events
        WHERE event_type='purchase'
        {brand_condition}
        {category_condition}""", engine)

if carts.iloc[0,0] > 0:
 abandonment_rate = ((carts.iloc[0,0] - purchases_count.iloc[0,0])/ carts.iloc[0,0]) * 100
else:
    abandonment_rate = 0


st.subheader("Conversion Funnel")
st.metric("Overall Cart Abandonment Rate", f"{abandonment_rate:.2f}%")

funnel = pd.DataFrame({
"Stage": ["View", "Cart", "Purchase"],
"Count": [
views.iloc[0,0],
carts.iloc[0,0],
purchases_count.iloc[0,0]
]
})
st.bar_chart(funnel.set_index("Stage"))

products = pd.read_sql(f"""SELECT product_id,
         COUNT(*) as purchases
         FROM events
         WHERE event_type='purchase'
         {brand_condition}
         {category_condition}
         GROUP BY product_id
         ORDER BY purchases DESC
         LIMIT 10""", engine)
st.subheader("Top Products")
st.dataframe(products)
st.bar_chart(products.set_index("product_id"))

st.subheader("Raw Event Data")
data = pd.read_sql(f"""
    SELECT *
       FROM events
       WHERE 1=1
       {brand_condition}
        {category_condition}
        {event_condition}
        LIMIT 100""", engine)
st.dataframe(data)

csv = data.to_csv(index=False)
st.download_button(
"Download Data",
csv,
"events.csv",
"text/csv"
)

active_users = pd.read_sql(f"""
    SELECT user_id,
    COUNT(*) as activity
    FROM events
    WHERE 1=1
    {brand_condition}
    {category_condition}
    GROUP BY user_id
    ORDER BY activity DESC
    LIMIT 10
    """, engine)
st.subheader("Most Active Users")
st.dataframe(active_users)

product_revenue = pd.read_sql(f"""
    SELECT product_id,
    ROUND(SUM(price),2) as revenue
    FROM events
    WHERE event_type='purchase'
    {brand_condition}
    {category_condition}
    GROUP BY product_id
    ORDER BY revenue DESC
    LIMIT 10
    """, engine)

st.subheader("Highest Revenue Products")
st.dataframe(product_revenue)
st.bar_chart(product_revenue.set_index("product_id"))

st.subheader("Dashboard Summary")
col1, col2 = st.columns(2)
with col1:
 st.bar_chart(top_brands.set_index("brand"))
with col2:
 st.bar_chart(categories.set_index("category_code"))

st.subheader("Business Insights")
st.info("""
• Most users only view products and do not purchase.
• Cart abandonment rate is high.
• A few brands generate most purchases.
• Some products generate significantly more revenue than others.
""")
st.subheader("Dataset Information")
st.write("Dataset: 2019-Nov E-Commerce Events")
st.write("Rows: Millions of customer interactions")
st.write("Source: Real E-Commerce Clickstream Dataset")
st.divider()
st.caption("Developed by Aishwarya Hada | Python • SQLite • Pandas • Streamlit")
