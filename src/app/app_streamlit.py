import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.rag.rag_system import PerfectRAGSystem

@st.cache_resource
def load_rag_system():
    return PerfectRAGSystem()

def initialize_chat():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "rag" not in st.session_state:
        st.session_state.rag = load_rag_system()

def display_chat():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("context"):
                with st.expander("View sources"):
                    st.write(message["context"])

def handle_user_input():
    if prompt := st.chat_input("Ask about the knowledge base..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            with st.spinner("Searching knowledge base..."):
                answer, context = st.session_state.rag.query(prompt)
                st.markdown(answer)
                with st.expander("View sources"):
                    st.write(context)
            
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "context": context
        })

def main():
    st.set_page_config(page_title="Knowledge Base Chat", page_icon="💬")
    st.title("💬 Knowledge Base Chatbot")
    st.caption("Ask questions about the content in the knowledge base")
    
    initialize_chat()
    display_chat()
    handle_user_input()

if __name__ == "__main__":
    main()