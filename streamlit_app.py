from openai import OpenAI
import streamlit as st
client = OpenAI(
  base_url=st.secrets["BASE_URL"],
  api_key=st.secrets["API_KEY"],
)
response = client.responses.create(
    model="nvidia/llama-3.1-nemotron-ultra-253b-v1:free",
    instructions="You are a coding assistant that talks like a pirate.",
    input="How do I check if a Python object is an instance of a class?",
)

