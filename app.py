"""Streamlit app for displaying members data."""

import pandas as pd
import streamlit as st

st.title("セレクトビュー")

# Load data
df = pd.read_csv("data/members.csv")

# Display data
st.dataframe(df)

st.markdown("---")
st.subheader("AI 分析")

prompt = st.text_area("分析依頼を入力してください", value="営業本部の男女比率は?")

if st.button("AI 分析開始"):
    if prompt:
        from agent_client import invoke_streaming

        st.write_stream(invoke_streaming(prompt))
    else:
        st.warning("分析依頼を入力してください。")
