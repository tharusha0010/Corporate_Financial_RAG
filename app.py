import streamlit as st
import requests

st.set_page_config(page_title="Financial RAG Chatbot", page_icon="📈", layout="centered")
st.title("📈 Corporate Financial RAG Chatbot")
st.caption("Ask any question from the Tesla 2023 Financial Report (Form 10-K)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Enter your financial question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing financial report... Please wait."):
            try:
                response = requests.post("http://127.0.0.1:8000/ask", json={"query": prompt})
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    sources = data["sources"]
                    
                    formatted_response = f"{answer}\n\n"
                    if sources:
                        formatted_response += "### 📚 Sources & Snippets:\n"
                        for i, src in enumerate(sources):
                            formatted_response += f"**[{i+1}] Page {src['page_num']}** (Score: `{src['score']:.4f}`)\n"
                            formatted_response += f"> _{src['snippet']}_\n\n"
                    
                    st.markdown(formatted_response)
                    st.session_state.messages.append({"role": "assistant", "content": formatted_response})
                else:
                    st.error(f"Error: API returned status code {response.status_code}")
            
            except requests.exceptions.ConnectionError:
                st.error("🚨 Connection Error: Cannot reach the FastAPI backend. Please make sure `api.py` is running in another terminal.")