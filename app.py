"""Streamlit app for displaying members data."""

import pandas as pd
import streamlit as st

st.title("セレクトビュー")

# Load data
df = pd.read_csv("data/members.csv")

# Display data
st.dataframe(df)
