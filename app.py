import streamlit as st
import requests

st.set_page_config(page_title="Financial RAG System", page_icon="📈", layout="centered")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_processed" not in st.session_state:
    st.session_state.is_processed = False
if "active_pdfs" not in st.session_state:
    st.session_state.active_pdfs = []

with st.sidebar:
    st.title("📈 Financial AI")
    st.write("Upload corporate financial documents for analysis.")
    st.divider()

    st.write("📄 **Upload your PDFs**")
    
    # accept_multiple_files=True යෙදීම
    uploaded_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True, label_visibility="collapsed")

    if uploaded_files:
        for f in uploaded_files:
            st.info(f"📎 {f.name}")

        if st.button("⚙️ Process PDFs", use_container_width=True):
            with st.spinner("Processing your documents..."):
                try:
                    # ෆයිල් කිහිපයක් එකවර යැවීමට සකස් කිරීම
                    files_payload = [("files", (f.name, f.getvalue(), "application/pdf")) for f in uploaded_files]
                    response = requests.post("http://127.0.0.1:8000/upload", files=files_payload)
                    
                    if response.status_code == 200:
                        st.session_state.is_processed = True
                        st.session_state.active_pdfs = [f.name for f in uploaded_files]
                        st.success("✅ PDFs processed successfully!")
                    else:
                        st.error("Error: Failed to process PDFs on backend.")
                except Exception as e:
                    st.error(f"Connection error: {e}")
            
    if st.session_state.is_processed:
        st.divider()
        st.success("📄 **Active documents:**\n\n" + "\n".join([f"- {name}" for name in st.session_state.active_pdfs]))

    st.divider()
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.title("📈 Corporate Financial RAG")
st.write("Intelligent retrieval and synthesis of corporate financial data.")

if not st.session_state.is_processed:
    st.info("👈 Upload financial documents (e.g., 10-K reports) from the sidebar to get started.")
    st.markdown("""
    ### How it works
    1. 📄 **Upload one or more PDFs**
    2. ⚙️ **Process the documents**
    3. 💬 **Ask financial questions**
    4. 🤖 **Get accurate, data-driven answers**
    """)
    
else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about the financial documents..."):
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
                    
                    if sources:
                        bot_response += "\n\n**Sources:**"
                        for src in sources:
                            bot_response += f"\n- Page {src['page_num']} (Score: {src['score']:.2f}): {src['snippet']}"
                else:
                    bot_response = "Error: Failed to connect to the backend API."
            except Exception as e:
                bot_response = f"Connection error: {e}"
        
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        with st.chat_message("assistant"):
            st.markdown(bot_response)