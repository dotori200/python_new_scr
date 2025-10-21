# pip install sqlalchemy pymysql
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import os

st.set_page_config(page_title="차량 FAQ", layout="wide")
st.title("🚗 차량 FAQ")

with st.container(horizontal=True, 
                  gap="medium",border=True
                  ):
    st.button("ALL")
    st.button("전기차")
    st.button("하이브리드")

DB_URL = os.getenv("DB_URL", "mysql+pymysql://root:root1234@localhost:3306/car_db?charset=utf8mb4")
engine = create_engine(DB_URL)

with engine.connect() as conn:
    rows = conn.execute(text("""
        SELECT company, COALESCE(category,'TOP10') AS category, question, answer
        FROM faq_top10
        WHERE company='Kia'
        ORDER BY id ASC
        LIMIT 10
    """)).fetchall()

df = pd.DataFrame(rows, columns=["company","category","question","answer"])

for i, r in df.iterrows():
    with st.expander(f"{i+1}. {r['question']}"):
        st.write(r['answer'])

