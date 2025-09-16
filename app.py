import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="🏏 Cricket SQL Dashboard", layout="wide")
st.title("🏏 Cricket SQL Dashboard")

# Connect to DB
try:
    conn = sqlite3.connect('cricket.db')
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    tables = pd.read_sql(query, conn)

    if not tables.empty:
        st.sidebar.header("📋 Select Table")
        table_names = tables['name'].tolist()
        selected_table = st.sidebar.selectbox("Choose a table", table_names)

        st.write(f"### Showing data from `{selected_table}`")
        df = pd.read_sql(f"SELECT * FROM {selected_table}", conn)
        st.dataframe(df, use_container_width=True)

        # Optional: SQL query input
        st.write("### 🧠 Run Custom SQL Query")
        user_query = st.text_area("Write your SQL query below", f"SELECT * FROM {selected_table} LIMIT 5;")
        if st.button("Run Query"):
            try:
                result = pd.read_sql(user_query, conn)
                st.success("Query executed successfully!")
                st.dataframe(result, use_container_width=True)
            except Exception as e:
                st.error(f"Query failed: {e}")
    else:
        st.warning("No tables found in cricket.db")

except Exception as e:
    st.error(f"Database error: {e}")

finally:
    conn.close()
