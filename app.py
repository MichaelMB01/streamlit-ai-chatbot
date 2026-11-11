import streamlit as st

from groq import Groq

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("My AI Chat Assistant")

st.sidebar.title("AI Chat Assistant")

st.sidebar.write("Your personal AI-powered chat assistant.")

st.sidebar.divider()

st.sidebar.write("Model: openai/gpt-oss-20b")

st.write("Welcome! Ask me anything.")


if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", 
    "content": "Hello! How can I assist you today?"})

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", 
    "content": "Hello! How can I assist you today?"})
    st.rerun()



for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input("Type your message")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    try:
        response = ""
        chat_completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
            ] + st.session_state.messages,
                stream=True
        )
        with st.spinner("Generating response..."):
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                for chunk in chat_completion:
                    if chunk.choices[0].delta.content:
                        response += chunk.choices[0].delta.content
                        response_placeholder.markdown(response)
    
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })     
    except Exception as e:
        st.error("Sorry, something went wrong. Please try again.")
        print("Error:", e)
