import streamlit as st
from sqlalchemy import create_engine, text
import os

DB_URL = os.getenv("DB_URL")  # mysql+pymysql://user:pw@host:3306/car_db?charset=utf8mb4
engine = create_engine(DB_URL)

st.title("연료별 자동차 등록 현황")

with engine.connect() as conn:
    rows = conn.execute(text("""
        SELECT year_month, fuel, SUM(count) AS cnt
        FROM fuel_registration
        WHERE vehicle_type='전체' AND fuel <> '소계'
        GROUP BY year_month, fuel
        ORDER BY year_month, fuel
    """)).fetchall()

import pandas as pd
df = pd.DataFrame(rows, columns=["year_month","fuel","cnt"])
st.dataframe(df)
st.line_chart(df.pivot(index="year_month", columns="fuel", values="cnt"))
