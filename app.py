import streamlit as st
import requests

st.set_page_config(page_title="OmniDoc-RAG", page_icon="📚", layout="centered")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_processed" not in st.session_state:
    st.session_state.is_processed = False
if "active_files" not in st.session_state:
    st.session_state.active_files = []

with st.sidebar:
    st.title("📚 OmniDoc-RAG")
    st.write("Upload your PDF, TXT, or CSV documents for intelligent analysis and Q&A.")
    st.divider()

    st.write("📄 **Upload your Documents**")
    
    uploaded_files = st.file_uploader(
        "Upload Documents", 
        type=["pdf", "txt", "csv"], 
        accept_multiple_files=True, 
        label_visibility="collapsed"
    )

    if uploaded_files:
        for f in uploaded_files:
            st.info(f"📎 {f.name}")

        if st.button("⚙️ Process Documents", use_container_width=True):
            with st.spinner("Processing your documents..."):
                try:
                    files_payload = []
                    for f in uploaded_files:
                        if f.name.endswith(".pdf"):
                            mime = "application/pdf"
                        elif f.name.endswith(".txt"):
                            mime = "text/plain"
                        elif f.name.endswith(".csv"):
                            mime = "text/csv"
                        else:
                            mime = "application/octet-stream"
                            
                        files_payload.append(("files", (f.name, f.getvalue(), mime)))
                        
                    response = requests.post("http://127.0.0.1:8000/upload", files=files_payload)
                    
                    if response.status_code == 200:
                        st.session_state.is_processed = True
                        st.session_state.active_files = [f.name for f in uploaded_files]
                        st.success("✅ Documents processed successfully!")
                    else:
                        st.error("Error: Failed to process documents on backend.")
                except Exception as e:
                    st.error(f"Connection error: {e}")
            
    if st.session_state.is_processed:
        st.divider()
        st.success("📄 **Active documents:**\n\n" + "\n".join([f"- {name}" for name in st.session_state.active_files]))

    st.divider()
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.title("📚 OmniDoc-RAG System")
st.write("Upload any PDF, TXT, or CSV document, ask questions, and get accurate, data-driven answers.")

if not st.session_state.is_processed:
    st.info("👈 Upload your documents from the sidebar to get started.")
    st.markdown("""
    ### How it works
    1. 📄 **Upload one or more PDFs, TXTs, or CSVs**
    2. ⚙️ **Process the documents**
    3. 💬 **Ask questions**
    4. 🤖 **Get answers with exact citations**
    """)
    
else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about the uploaded documents..."):
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
                    data = response.json()
                    bot_response = data.get("answer", "No answer found.")
                    sources = data.get("sources", [])
                    
                    
                    if sources and len(sources) > 0:
                        bot_response += "\n\n**Sources:**"
                        for src in sources:
                            file_name = src.get('file_name', 'Unknown Document')
                            bot_response += f"\n- **{file_name}** | Page {src['page_num']} (Score: {src['score']:.2f}): {src['snippet']}"
                else:
                    bot_response = "Error: Failed to connect to the backend API."
            except Exception as e:
                bot_response = f"Connection error: {e}"
        
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        with st.chat_message("assistant"):
            st.markdown(bot_response)