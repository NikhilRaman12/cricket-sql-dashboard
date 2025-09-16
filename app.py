import streamlit as st
import pandas as pd
import sqlite3
import requests

st.set_page_config(page_title="🏏 Cricket SQL Dashboard", layout="wide")

# Sidebar navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", [
    "Home",
    "Live Matches",
    "Top Player Stats",
    "SQL Analytics",
    "CRUD Operations"
])

# --- HOME PAGE ---
def show_home():
    st.title("🏏 Cricbuzz LiveStats Dashboard")
    st.markdown("""
    This dashboard provides interactive cricket analytics using SQL and real-time data.
    
    **Modules Included:**
    - Live match updates
    - Top player statistics
    - SQL query interface
    - CRUD operations on player data

    **Tech Stack:** Python, Streamlit, SQLite, Pandas, Requests
    """)

# --- LIVE MATCH PAGE ---
def show_live_matches():
    st.title("🏟️ Live Matches")
    st.info("This section will display live match data from Cricbuzz API.")
    st.warning("API integration pending. Placeholder only.")
    # Uncomment and configure when API key is ready
    # url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"
    # headers = {
    #     "X-RapidAPI-Key": st.secrets["RAPIDAPI_KEY"],
    #     "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
    # }
    # try:
    #     response = requests.get(url, headers=headers)
    #     data = response.json()
    #     st.json(data)
    # except Exception as e:
    #     st.error(f"API error: {e}")

# --- TOP PLAYER STATS PAGE ---
def show_top_stats():
    st.title("🌟 Top Player Stats")
    st.info("This section will show top batting and bowling stats.")
    st.warning("API integration pending. Placeholder only.")

# --- SQL ANALYTICS PAGE ---
def show_sql_analytics():
    st.title("🧠 SQL Analytics")

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

# --- CRUD OPERATIONS PAGE ---
def show_crud_operations():
    st.title("✍️ Manage Player Records")

    try:
        conn = sqlite3.connect("cricket.db")
        cursor = conn.cursor()

        st.subheader("Add New Player")
        with st.form("add_player"):
            name = st.text_input("Full Name")
            role = st.selectbox("Playing Role", ["Batsman", "Bowler", "All-Rounder"])
            batting = st.text_input("Batting Style")
            bowling = st.text_input("Bowling Style")
            team = st.text_input("Team Name")
            submitted = st.form_submit_button("Add Player")

            if submitted:
                try:
                    cursor.execute("""
                        INSERT INTO players (full_name, playing_role, batting_style, bowling_style, team_name)
                        VALUES (?, ?, ?, ?, ?)
                    """, (name, role, batting, bowling, team))
                    conn.commit()
                    st.success("Player added successfully.")
                except Exception as e:
                    st.error(f"Insert failed: {e}")

        st.subheader("Current Players")
        try:
            players_df = pd.read_sql("SELECT * FROM players", conn)
            st.dataframe(players_df, use_container_width=True)
        except Exception as e:
            st.error(f"Failed to load players: {e}")

    except Exception as e:
        st.error(f"Database error: {e}")

    finally:
        conn.close()

# --- PAGE ROUTING ---
if page == "Home":
    show_home()
elif page == "Live Matches":
    show_live_matches()
elif page == "Top Player Stats":
    show_top_stats()
elif page == "SQL Analytics":
    show_sql_analytics()
elif page == "CRUD Operations":
    show_crud_operations()
