import streamlit as st
import os
from query import AgriAssistQuery

# PAGE CONFIG
st.set_page_config(
    page_title="AgriAssist - AI Farming Assistant",
    page_icon="🌾",
    layout="wide"
)

st.markdown(
    """
    <style>
    .main-container {
        padding: 20px;
    }

    /* Weather Card */
    .weather-card {
        background-color: #fff5e5;
        padding: 18px;
        border-radius: 12px;
        border-left: 5px solid #ffaa2b;
        margin-bottom: 15px;
        color: #333333 !important; /* DARK TEXT */
    }

    /* Answer Box */
    .answer-box {
        background-color: #f8f8f8;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #ddd;
        color: #222222 !important;  /* DARK TEXT */
        font-size: 1.05rem;
        line-height: 1.6;
    }

    /* Sources Box */
    .source-box {
        background-color: #eaf4ff;
        padding: 15px;
        border-radius: 10px;
        margin-top: 10px;
        border-left: 4px solid #2b8aff;
        color: #1a1a1a !important; /* DARK TEXT */
        font-size: 0.9rem;
    }

    /* Label colors */
    h4, h3, h2, h1, label {
        color: #FF9600 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------------------
# 🌿 TITLE
# --------------------------------------------------------------
st.title("🌾 AgriAssist — Smart Agriculture Q&A with Gemini 2.5 Pro")

# --------------------------------------------------------------
# 🌿 INITIALIZE SYSTEM (cached)
# --------------------------------------------------------------
@st.cache_resource
def load_system():
    return AgriAssistQuery()

qa_system = load_system()

# --------------------------------------------------------------
# 🌿 SIDEBAR SETTINGS
# --------------------------------------------------------------
st.sidebar.header("⚙️ Settings")

include_weather = st.sidebar.checkbox("Enable Weather", value=True)

location = st.sidebar.text_input("Enter City for Weather:", value="Delhi")

st.sidebar.markdown("---")
st.sidebar.write("Built with **Gemini-2.5-Pro**, ChromaDB & Streamlit 💚")

# --------------------------------------------------------------
# 🌿 MAIN INPUT
# --------------------------------------------------------------
user_question = st.text_area(
    "Ask your farming question below:",
    placeholder="Example: What crops can I grow in monsoon?",
    height=120
)

if st.button("Get Answer", use_container_width=True):
    if not user_question.strip():
        st.warning("Please enter a question!")
        st.stop()

    # Process Query
    with st.spinner("🌱 Thinking… Fetching info from PDFs + Gemini…"):
        response = qa_system.answer_query(
            question=user_question,
            location=location,
            include_weather=include_weather
        )

    # ----------------------------------------------------------
    # 🌦 WEATHER OUTPUT
    # ----------------------------------------------------------
    if include_weather and response["weather"]:
        w = response["weather"]
        st.markdown(
            f"""
            <div class="weather-card">
                <h4>🌦 Weather in {response['location']}</h4>
                <b>Temperature:</b> {w['temperature']}°C<br>
                <b>Humidity:</b> {w['humidity']}<br>
                <b>Condition:</b> {w['description']}<br>
                <b>Rainfall:</b> {w['rainfall']} mm
            </div>
            """,
            unsafe_allow_html=True
        )

    # ----------------------------------------------------------
    # 🌿 FINAL ANSWER
    # ----------------------------------------------------------
    st.markdown("### 🧠 Answer")
    st.markdown(
        f"<div class='answer-box'>{response['answer']}</div>",
        unsafe_allow_html=True
    )

    # ----------------------------------------------------------
    # 📘 SOURCES
    # ----------------------------------------------------------
    if response["sources"]:
        st.markdown("### 📘 Sources Used")
        for src in response["sources"]:
            st.markdown(
                f"<div class='source-box'>{src}</div>",
                unsafe_allow_html=True
            )

# --------------------------------------------------------------
# FOOTER
# --------------------------------------------------------------
st.markdown("---")
st.markdown(
    "<center>🌱 Built with ❤️ for farmers using Gemini-2.5-Pro + RAG</center>",
    unsafe_allow_html=True
)
