import streamlit as st
import requests
import pandas as pd

from src.config import BACKEND_URL
from src.charts import chart_daily_stock

st.set_page_config(page_title='Stock balance', layout='wide')

# Define session_state
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "input" not in st.session_state:
    st.session_state["input"] = ""
if "stored_session" not in st.session_state:
    st.session_state["stored_session"] = []


st.title("Stock balance")

# % ingresos sobre gasto
items = requests.get(BACKEND_URL + 'items').json()

items = [item['item_id'] for item in items]

item_id = st.selectbox('Select the item', items)

daily_stock = requests.get(BACKEND_URL + f'daily_stock/{item_id}').json()

df = pd.DataFrame(daily_stock)
fig = chart_daily_stock(df)
st.plotly_chart(fig)