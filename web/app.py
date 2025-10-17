import streamlit as st
import requests
import os
import logging as log
log.basicConfig(level=log.INFO, 
                format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                datefmt='%Y-%m-%dT%H:%M:%S')

log.info("Starting web app")
log.info(f'LLM Model URL: {os.environ['LLM_URL']}')
log.info(f'LLM Model NAME: {os.environ['LLM_MODEL']}')

# base_url = os.environ['LLM_URL']
base_url = 'http://model-runner.docker.internal:12434'

# completions_url = f"{ base_url }/engines/llama.cpp/v1/chat/completions"
completions_url = f"{ base_url }/engines/v1/chat/completions"
log.info(f'Completions url: {completions_url}')


st.title("LLM Chatbot")

user_input = st.text_input("Your message:")
log.info(f'Got user input: {user_input}')
if st.button("Send") and user_input:
    try:
        log.info(f'Sending request to user')

        response = requests.post(
            completions_url,
            json={
                "model": os.environ['LLM_MODEL'],
                "messages": [
                {"role": "user", "content": user_input}
                ]
            }
        )

        if response.status_code == 200:
            data = response.json()
            if "choices" in data and len(data["choices"]) > 0:
                llm_answer = data["choices"][0]["message"]["content"]
                log.info(f"🤖 Answer: {llm_answer}")
                st.markdown(f"**🤖 Answer:** {llm_answer}")
            else:
                st.markdown(f"**🤖 Unexpected error:** {data}")
                log.error(f"Unexpected response: {data}")
            
        else:
            st.error(f"Error from LLM: {response.text}")
        
    except Exception as e:
        st.error(f"Could not reach LLM service: {e}")
