import os
import html
import uuid
import streamlit as st

# ============================================================
# BACKEND IMPORTS
# ============================================================
from src.load_document import load_pdf
from src.chunk_text import split_text
from src.embeddings import create_vectorstore
from src.retrieve import retrieve_documents
from src.chatbot import generate_answer


# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="DocuMind",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# LOAD CSS
# ============================================================
if os.path.exists("style.css"):
    with open("style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = None

if "chunks" not in st.session_state:
    st.session_state.chunks = None

if "index" not in st.session_state:
    st.session_state.index = None

if "document_name" not in st.session_state:
    st.session_state.document_name = None

if "processed" not in st.session_state:
    st.session_state.processed = False


def save_active_chat():
    if not st.session_state.messages:
        return

    chat_id = st.session_state.active_chat_id
    conversation = next(
        (chat for chat in st.session_state.chat_history if chat["id"] == chat_id),
        None,
    )

    if conversation is None:
        chat_id = uuid.uuid4().hex
        st.session_state.active_chat_id = chat_id
        first_question = next(
            message["content"]
            for message in st.session_state.messages
            if message["role"] == "user"
        )
        title = " ".join(str(first_question).split())
        if len(title) > 36:
            title = title[:33] + "..."
        conversation = {"id": chat_id, "title": title}
        st.session_state.chat_history.insert(0, conversation)

    conversation["messages"] = [message.copy() for message in st.session_state.messages]
    conversation["document_name"] = st.session_state.document_name
    conversation["chunks"] = st.session_state.chunks
    conversation["index"] = st.session_state.index


if st.session_state.messages and st.session_state.active_chat_id is None:
    save_active_chat()


# ============================================================
# LOGIN PAGE
# ============================================================
if not st.session_state.logged_in:
    with st.container(key="login-card"):
        st.markdown(
            """
            <div class="login-container">
                <div class="login-logo">✦</div>
                <div class="login-title">Welcome to DocuMind</div>
                <div class="login-subtitle">Your AI-powered document assistant</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            key="login_username",
        )
        show_password = st.session_state.get("show_login_password", False)
        password = st.text_input(
            "Password",
            type="default" if show_password else "password",
            placeholder="Enter your password",
            key="login_password",
        )
        st.checkbox("Show password", key="show_login_password")
        login = st.button("Login →", use_container_width=True)

        if login:
            if username and password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Please enter username and password.")

    st.markdown(
        """
        <div class="login-footer">
            DocuMind AI • Secure Document Chat
        </div>
        """,
        unsafe_allow_html=True
    )
    st.stop()


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown(
        """
        <div class="wa-brand">
            <div class="wa-brand-icon">✦</div>
            <div>
                <div class="wa-brand-name">DocuMind</div>
                <div class="wa-brand-subtitle">AI Document Assistant</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="sidebar-search">🔍 Search chats</div>', unsafe_allow_html=True)
    st.markdown('<div class="chat-section-title">CHATS</div>', unsafe_allow_html=True)

    if st.session_state.processed:
        st.markdown(
            f"""
            <div class="chat-list-item active">
                <div class="chat-file-icon">📄</div>
                <div class="chat-preview">
                    <div class="chat-file-name">{html.escape(st.session_state.document_name)}</div>
                    <div class="chat-preview-text">Document ready to chat</div>
                </div>
                <div class="chat-status">●</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown('<div class="empty-chat">No document uploaded</div>', unsafe_allow_html=True)

    st.markdown('<div class="chat-section-title">RECENT CHATS</div>', unsafe_allow_html=True)
    if st.session_state.chat_history:
        for conversation in st.session_state.chat_history:
            title = html.escape(conversation["title"])
            if st.button(
                f"💬 {title}",
                key=f"history-{conversation['id']}",
                help=conversation.get("document_name") or "Document chat",
                use_container_width=True,
            ):
                st.session_state.active_chat_id = conversation["id"]
                st.session_state.messages = [
                    message.copy() for message in conversation["messages"]
                ]
                st.session_state.document_name = conversation.get("document_name")
                st.session_state.chunks = conversation.get("chunks")
                st.session_state.index = conversation.get("index")
                st.session_state.processed = bool(
                    st.session_state.chunks is not None
                    and st.session_state.index is not None
                )
                st.rerun()
    else:
        st.markdown('<div class="empty-chat">No saved chats yet</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="chat-section-title">DOCUMENT</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")

    if uploaded_file:
        os.makedirs("data", exist_ok=True)

        # safe unique file name
        safe_name = uploaded_file.name.replace(" ", "_")
        file_path = os.path.join("data", safe_name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.markdown(
            f"""
            <div class="uploaded-file">
                <div class="uploaded-icon">📄</div>
                <div>
                    <div class="uploaded-name">{html.escape(uploaded_file.name)}</div>
                    <div class="uploaded-type">PDF DOCUMENT</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("Process Document", use_container_width=True):
            with st.spinner("Processing document..."):
                text = load_pdf(file_path)
                chunks = split_text(text)
                index, _ = create_vectorstore(chunks)

                st.session_state.chunks = chunks
                st.session_state.index = index
                st.session_state.document_name = uploaded_file.name
                st.session_state.processed = True
                st.session_state.messages = []
                st.session_state.active_chat_id = None

            st.success(f"{len(chunks)} chunks indexed")
            st.rerun()

    st.markdown("---")

    if st.button("＋ New conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.active_chat_id = None
        st.rerun()

    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.messages = []
        st.session_state.active_chat_id = None
        st.rerun()


# ============================================================
# MAIN CHAT AREA
# ============================================================
document_title = st.session_state.document_name if st.session_state.document_name else "DocuMind AI"

st.markdown(
    f"""
    <div class="chat-header">
        <div class="chat-header-avatar">📄</div>
        <div class="chat-header-info">
            <div class="chat-header-title">{html.escape(document_title)}</div>
            <div class="chat-header-status">● DocuMind AI</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# Welcome message
if not st.session_state.messages:
    st.markdown(
        """
        <div class="welcome-message">
            <div class="welcome-icon">✦</div>
            <div class="welcome-title">Welcome to DocuMind AI</div>
            <div class="welcome-text">
                Upload a PDF and ask questions about your document.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# Chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        safe_message = html.escape(str(message["content"]))
        st.markdown(
            f"""
            <div class="message-row user-row">
                <div class="user-message">{safe_message}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        safe_message = html.escape(str(message["content"]))
        st.markdown(
            f"""
            <div class="message-row ai-row">
                <div class="ai-avatar">✦</div>
                <div class="ai-message">
                    <div class="ai-name">DocuMind AI</div>
                    <div class="ai-text">{safe_message}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# Chat input
question = st.chat_input("Type a message...")

if question:
    if st.session_state.chunks is None or st.session_state.index is None:
        st.warning("Please upload and process a PDF first.")
    else:
        st.session_state.messages.append({"role": "user", "content": question})
        save_active_chat()

        with st.spinner("Searching document..."):
            relevant_chunks = retrieve_documents(
                question,
                st.session_state.chunks,
                st.session_state.index,
                top_k=2
            )

        context = "\n\n".join(relevant_chunks)

        with st.spinner("DocuMind is thinking..."):
            answer = generate_answer(question, context)

        st.session_state.messages.append({"role": "assistant", "content": answer})
        save_active_chat()
        st.rerun()