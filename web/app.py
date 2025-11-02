import streamlit as st
import requests
import os
import random
import time
import logging as log
from llm import stream_llm_response

log.basicConfig(level=log.INFO, 
                format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                datefmt='%Y-%m-%dT%H:%M:%S')

log.info("Starting web app")
# log.info(f'LLM Model URL: {os.environ['LLM_URL']}')
log.info(f'LLM Model NAME: {os.environ['LLM_MODEL']}')

# base_url = 'http://model-runner.docker.internal:12434'
base_url = os.environ['LLM_BASE_URL']

completions_url = f"{ base_url }/v1/chat/completions"
log.info(f'Completions url: {completions_url}')

st.write(f"LLM Model: {os.environ['LLM_MODEL']}")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Let's start chatting! 👇"}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask anything"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for chunk in stream_llm_response(completions_url, os.environ['LLM_MODEL'], prompt):
            full_response += chunk
            time.sleep(0.05)
            if chunk.startswith("[ERROR]") or chunk.startswith("[EXCEPTION]"):
                st.error(chunk)
                break

            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
