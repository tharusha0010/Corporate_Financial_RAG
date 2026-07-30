import streamlit as st
import requests

st.set_page_config(page_title="Financial RAG System", page_icon="📈", layout="centered")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_processed" not in st.session_state:
    st.session_state.is_processed = False
if "active_pdf" not in st.session_state:
    st.session_state.active_pdf = ""

with st.sidebar:
    st.title("📈 Financial AI")
    st.write("Upload a corporate financial document for analysis.")
    st.divider()

    st.write("📄 **Upload your PDF**")
    
    uploaded_file = st.file_uploader("Upload PDF", type="pdf", label_visibility="collapsed")

    if uploaded_file is not None:
        st.info(f"📎 {uploaded_file.name}")

        if st.button("⚙️ Process PDF", use_container_width=True):
            with st.spinner("Processing your document..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    response = requests.post("http://127.0.0.1:8000/upload", files=files)
                    
                    if response.status_code == 200:
                        st.session_state.is_processed = True
                        st.session_state.active_pdf = uploaded_file.name
                        st.success("✅ PDF processed successfully!")
                    else:
                        st.error("Error: Failed to process PDF on backend.")
                except Exception as e:
                    st.error(f"Connection error: {e}")
            
    if st.session_state.is_processed:
        st.divider()
        st.success(f"📄 **Active document:**\n\n{st.session_state.active_pdf}")

    st.divider()
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.title("📈 Corporate Financial RAG")
st.write("Intelligent retrieval and synthesis of corporate financial data.")

if not st.session_state.is_processed:
    st.info("👈 Upload a financial document (e.g., 10-K report) from the sidebar to get started.")
    st.markdown("""
    ### How it works
    1. 📄 **Upload a PDF**
    2. ⚙️ **Process the document**
    3. 💬 **Ask financial questions**
    4. 🤖 **Get accurate, data-driven answers**
    """)
    
else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about the financial document..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Generating answer..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/ask", 
                    json={"question": prompt}
                )
                
                if response.status_code == 200:
                    bot_response = response.json().get("answer", "No answer found.")
                else:
                    bot_response = "Error: Failed to connect to the backend API."
            except Exception as e:
                bot_response = f"Connection error: {e}"
        
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        with st.chat_message("assistant"):
            st.markdown(bot_response)