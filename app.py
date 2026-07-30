import streamlit as st
import time

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
    
    uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")

    if uploaded_file is not None:
        st.info(f"📎 {uploaded_file.name}")

        if st.button("⚙️ Process PDF", use_container_width=True):
            with st.spinner("Processing your document..."):
                time.sleep(3) 
                
                st.session_state.is_processed = True
                st.session_state.active_pdf = uploaded_file.name
            
            st.success("✅ PDF processed successfully!")
            
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

        bot_response = f"This is an answer based on {st.session_state.active_pdf}. You asked: {prompt}"
        
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        with st.chat_message("assistant"):
            st.markdown(bot_response)