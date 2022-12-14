import pandas as pd
import sqlite3

# Load exsited file
df = pd.read_csv("./NTU_GYM_Counter.csv", index_col='Timestamp')

# Create sql file
conn = sqlite3.connect("./database")
cursor = conn.cursor()

# Convert Pandas df to sql
df.to_sql(name='db', con=conn)
conn.close()
