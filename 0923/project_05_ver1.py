# pip install pymysql pandas
import pandas as pd, pymysql

df = pd.read_csv("kia_faq_top10.csv")  # columns: company, category, question, answer

conn = pymysql.connect(host="localhost", user="root", password="root1234", db="car_db", charset="utf8mb4")
cur = conn.cursor()
cur.executemany(
    "INSERT IGNORE INTO faq_top10 (company, category, question, answer) VALUES (%s,%s,%s,%s)",
    df[["company","category","question","answer"]].values.tolist()
)
conn.commit()
cur.close(); conn.close()
print("MySQL 저장 완료")