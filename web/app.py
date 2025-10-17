import streamlit as st
import requests
import os
import random
import time
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


    try:
        log.info(f'Sending request to user')

        response = requests.post(
            completions_url,
            json={
                "model": os.environ['LLM_MODEL'],
                "messages": [
                {"role": "user", "content": prompt}
                ]
            }
        )
        full_response = ""
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            if response.status_code == 200:
                data = response.json()
                if "choices" in data and len(data["choices"]) > 0:
                    llm_answer = data["choices"][0]["message"]["content"]
                    log.info(f"🤖 Answer: {llm_answer}")
                    # st.markdown(f"**🤖 Answer:** {llm_answer}")
                    message_placeholder.markdown(llm_answer)
                else:
                    message_placeholder.markdown(f"**🤖 Unexpected error:** {data}")
                    log.error(f"Unexpected response: {data}")
                
            else:
                message_placeholder.markdown(f"**🤖 Unexpected error:** {response.text}")
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
    except Exception as e:
        st.error(f"Could not reach LLM service: {e}")

    # Display assistant response in chat message container
    # with st.chat_message("assistant"):
    #     message_placeholder = st.empty()
    #     full_response = ""
    #     assistant_response = random.choice(
    #         [
    #             "Hello there! How can I assist you today?",
    #             "Hi, human! Is there anything I can help you with?",
    #             "Do you need help?",
    #         ]
    #     )
    #     # Simulate stream of response with milliseconds delay
    #     for chunk in assistant_response.split():
    #         full_response += chunk + " "
    #         time.sleep(0.05)
    #         # Add a blinking cursor to simulate typing
    #         message_placeholder.markdown(full_response + "▌")
    #     message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
