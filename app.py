import streamlit as st
import requests

st.set_page_config(
    page_title="Corporate Financial RAG Chatbot",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .main { background-color: #f8f9fa; }
        .stChatMessage { border-radius: 10px; padding: 10px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://img.icons8.com/color/96/combo-chart--v1.png", width=80)
    st.title("System Control")
    st.info("Connected to FastAPI RAG Backend.")
    
    if st.button("Clear Chat History", type="secondary"):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.markdown("**Model:** Gemma 3 (12B)")
    st.markdown("**Document:** Tesla 2023 10-K")

st.title("📈 Corporate Financial RAG Chatbot")
st.caption("Advanced AI assistant for querying corporate financial reports with high accuracy.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander("📚 View Retrieved Sources"):
                for idx, src in enumerate(message["sources"], 1):
                    st.markdown(f"**Source {idx}:**")
                    st.text(src)

if prompt := st.chat_input("Ask any question from the financial report..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing financial data..."):
            try:
                res = requests.post("http://127.0.0.1:8000/ask", json={"question": prompt})
                if res.status_code == 200:
                    data = res.json()
                    answer = data.get("answer", "No answer found.")
                    sources = data.get("sources", [])
                    
                    st.markdown(answer)
                    
                    if sources:
                        with st.expander("📚 View Retrieved Sources"):
                            for idx, src in enumerate(sources, 1):
                                st.markdown(f"**Source {idx}:**")
                                st.text(src)
                                
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": answer, 
                        "sources": sources
                    })
                else:
                    error_msg = f"Error: API returned status code {res.status_code}"
                    st.error(error_msg)
            except Exception as e:
                error_msg = f"Connection Error: Could not connect to backend. ({e})"
                st.error(error_msg)