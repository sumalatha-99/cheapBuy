import openai
import streamlit as st
openai_api_key = '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'

st.title("🧑‍💻 Skolo Online 💬 Chatbot")
"""
My name is Cercei Lannister🤖. 
I know many things, ask me anything you like, 
but please. Dont ask me stupid questions❓
"""
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a sacarstic assistant called Cercei Lannister, you love to use emojis."}
    ]
if prompt := st.chat_input():
    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    #response = openai.ChatCompletion.create(model="gpt-3.5-turbo-0613", messages=st.session_state.messages)
    #msg = response.choices[0].message
    msg = "this is new for me !!"
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg)