import streamlit as st
import pandas as pd
import pydeck as pdk
from sqlalchemy import create_engine, text

# Database connection
engine = create_engine("postgresql+psycopg2://postgres:12345@localhost:5433/flight_analytics")

# Page config
st.set_page_config(page_title="Air Tracker", page_icon="✈️", layout="wide")

# Helper function
def run_query(query):
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn)

# Sidebar navigation
page = st.sidebar.selectbox("Navigation", [
    "Homepage Dashboard",
    "Search & Filter Flights",
    "Airport Details",
    "Delay Analysis",
    "Route Leaderboards",
    "Airline Performance"
])

st.title("✈️ Air Tracker: Flight Analytics")

if page == "Homepage Dashboard":
    st.subheader("📊 Summary Statistics")

    total_airports = run_query("select count(*) as count from airport").iloc[0]['count']
    total_flights  = run_query("select count(*) as count from flights").iloc[0]['count']
    avg_delay      = run_query("select round(avg(avg_delay_min)::numeric, 2) as avg from airport_delays").iloc[0]['avg']

    st.subheader("🏅 Quick Insights")
    col4, col5, col6 = st.columns(3)

    busiest_airline      = run_query("select airline_code, count(flight_id) as total from flights group by airline_code order by total desc limit 1").iloc[0]
    most_delayed_airport = run_query("select airport_iata, avg_delay_min from airport_delays order by avg_delay_min desc limit 1").iloc[0]
    most_cancelled       = run_query("select airport_iata, canceled_flights from airport_delays order by canceled_flights desc limit 1").iloc[0]

    col4.metric("Busiest Airline", busiest_airline["airline_code"], f"{busiest_airline['total']} flights")
    col5.metric("Most Delayed Airport", most_delayed_airport["airport_iata"], f"{most_delayed_airport['avg_delay_min']} min")
    col6.metric("Most Cancellations", most_cancelled["airport_iata"], f"{most_cancelled['canceled_flights']} flights")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Airports", total_airports)
    col2.metric("Total Flights", total_flights)
    col3.metric("Avg Delay (min)", avg_delay)

    st.subheader("🗺️ Airport Locations")
    map_df = run_query('select latitude, longitude, "fullName", city from airport')

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_df,
        get_position=["longitude", "latitude"],
        get_color=[255, 75, 75, 200],
        get_radius=100000,
        pickable=True,
        auto_highlight=True,
    )
    view = pdk.ViewState(latitude=20, longitude=0, zoom=1.5)
    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view,
        tooltip={"text": "{fullName}\n{city}"},
        map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json"
    ))

elif page == "Search & Filter Flights":
    st.subheader("🔍 Search & Filter Flights")

    col1, col2 = st.columns(2)
    flight_number = col1.text_input("Flight Number")
    airline_code  = col2.text_input("Airline Code")

    col3, col4 = st.columns(2)
    status_options = ["All"] + run_query("select distinct status from flights")["status"].tolist()
    status = col3.selectbox("Status", status_options)
    origin = col4.text_input("Origin Airport (IATA)")

    query = "select flight_number, airline_code, origin_iata, destination_iata, scheduled_departure, scheduled_arrival, status from flights where 1=1"

    if flight_number:
        query += f" and flight_number ilike '%{flight_number}%'"
    if airline_code:
        query += f" and airline_code ilike '%{airline_code}%'"
    if status != "All":
        query += f" and status = '{status}'"
    if origin:
        query += f" and origin_iata ilike '%{origin}%'"

    df = run_query(query)
    st.dataframe(df, use_container_width=True)
    st.download_button(
        label="Download Results as CSV",
        data=df.to_csv(index=False),
        file_name="flights.csv",
        mime="text/csv"
    )
    st.caption(f"Showing {len(df)} flights")

elif page == "Airport Details":
    st.subheader("🏢 Airport Details Viewer")

    airports = run_query('select iata, "fullName" from airport order by "fullName"')
    selected = st.selectbox("Select Airport", airports["fullName"].tolist())
    iata = airports[airports["fullName"] == selected]["iata"].values[0]

    airport_info = run_query(f"select * from airport where iata = '{iata}'")

    col1, col2, col3 = st.columns(3)
    col1.metric("City", airport_info["city"].values[0])
    col2.metric("Country", airport_info["country_code"].values[0])
    col3.metric("Timezone", airport_info["timeZone"].values[0])

    st.subheader("Linked Flights")
    flights = run_query(f"select flight_number, origin_iata, destination_iata, scheduled_departure, status from flights where origin_iata = '{iata}' or destination_iata = '{iata}' limit 50")
    st.dataframe(flights, use_container_width=True)
    st.caption(f"Showing {len(flights)} flights")

elif page == "Delay Analysis":
    st.subheader("⏱️ Delay Analysis")

    delay_df = run_query("select * from airport_delays order by avg_delay_min desc")

    st.subheader("Average Delay by Airport (minutes)")
    st.bar_chart(delay_df.set_index("airport_iata")["avg_delay_min"])

    st.subheader("Cancelled Flights by Airport")
    st.bar_chart(delay_df.set_index("airport_iata")["canceled_flights"])

    st.subheader("Delay Statistics Table")
    st.dataframe(delay_df, use_container_width=True)

elif page == "Route Leaderboards":
    st.subheader("🏆 Route Leaderboards")

    st.subheader("Busiest Routes (Most Flights)")
    busiest_routes = run_query("""
        select origin_iata, destination_iata, count(flight_id) as total_flights
        from flights
        group by origin_iata, destination_iata
        order by total_flights desc
        limit 10
    """)
    st.dataframe(busiest_routes, use_container_width=True)

    st.subheader("Most Delayed Airports")
    most_delayed = run_query("""
        select airport_iata, avg_delay_min, delayed_flights, canceled_flights
        from airport_delays
        order by avg_delay_min desc
    """)
    st.dataframe(most_delayed, use_container_width=True)
    st.bar_chart(most_delayed.set_index("airport_iata")["delayed_flights"])

elif page == "Airline Performance":
    st.subheader("✈️ Airline Performance")

    airline_df = run_query("""
        select 
            airline_code,
            count(flight_id) as total_flights,
            count(case when status = 'Arrived' then 1 end) as arrived,
            count(case when status = 'Delayed' then 1 end) as delayed,
            count(case when status = 'Canceled' then 1 end) as cancelled,
            round(count(case when status = 'Delayed' then 1 end) * 100.0 / count(flight_id), 2) as delay_percentage
        from flights
        group by airline_code
        order by delay_percentage desc
    """)

    col1, col2 = st.columns(2)
    col1.metric("Most Punctual Airline", airline_df.iloc[-1]["airline_code"])
    col2.metric("Most Delayed Airline", airline_df.iloc[0]["airline_code"])

    st.subheader("Delay % by Airline")
    st.bar_chart(airline_df.set_index("airline_code")["delay_percentage"])

    st.subheader("Full Airline Stats")
    st.dataframe(airline_df, use_container_width=True)