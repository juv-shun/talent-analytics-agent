"""Streamlit app for displaying members data."""

import os

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
password = st.text_input("パスワードを入力してください", type="password")

if st.button("AI 分析開始"):
    agent_password = os.environ.get("AGENT_PASSWORD")
    if not agent_password:
        st.error("環境変数 AGENT_PASSWORD が設定されていません。")
    elif password != agent_password:
        st.error("パスワードが間違っています。")
    elif prompt:
        from agent_client import invoke_streaming

        st.write_stream(invoke_streaming(prompt))
    else:
        st.warning("分析依頼を入力してください。")
