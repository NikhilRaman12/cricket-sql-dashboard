import streamlit as st
import pandas as pd
import sqlite3

st.title("🏏 Cricket SQL Dashboard")

# Connect to your cricket.db
try:
    conn = sqlite3.connect('cricket.db')
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    tables = pd.read_sql(query, conn)
    st.write("### Tables in Database", tables)

    if not tables.empty:
        # Show data from the first table found
        first_table = tables.iloc[0,0]
        st.write(f"### Showing data from `{first_table}`")
        df = pd.read_sql(f"SELECT * FROM {first_table}", conn)
        st.dataframe(df)
    else:
        st.warning("No tables found in cricket.db")
except Exception as e:
    st.error(f"Database error: {e}")
finally:
    conn.close()
