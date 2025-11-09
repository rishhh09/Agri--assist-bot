# app.py - Cloud Ready Version
import streamlit as st
import json
import os
import sys

# Page config
st.set_page_config(
    page_title="AgriAssist - Farmer Q&A",
    page_icon="🌾",
    layout="wide"
)

# Check if database exists, if not create it
DB_DIRECTORY = "db"
if not os.path.exists(DB_DIRECTORY):
    st.warning("🔄 First time setup: Creating database... This may take 2-3 minutes.")
    st.info("📂 Processing PDFs from data folder...")
    
    try:
        # Import and run ingestion
        from langchain_community.document_loaders import PyPDFDirectoryLoader
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_community.embeddings import SentenceTransformerEmbeddings
        from langchain_community.vectorstores import Chroma
        
        with st.spinner("Loading PDFs..."):
            loader = PyPDFDirectoryLoader("data/")
            documents = loader.load()
            st.success(f"✓ Loaded {len(documents)} pages")
        
        with st.spinner("Splitting into chunks..."):
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = text_splitter.split_documents(documents)
            st.success(f"✓ Created {len(chunks)} chunks")
        
        with st.spinner("Creating vector database (this takes longest)..."):
            embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
            db = Chroma.from_documents(chunks, embedding_model, persist_directory=DB_DIRECTORY)
            st.success("✓ Database created!")
        
        st.balloons()
        st.info("🎉 Setup complete! Please refresh the page to start using AgriAssist.")
        st.stop()
        
    except Exception as e:
        st.error(f"❌ Error creating database: {e}")
        st.code(str(e))
        st.info("This might be due to memory limits on Streamlit Cloud. Try using fewer/smaller PDFs.")
        st.stop()

# Now load the query system
try:
    from query import AgriAssistQuery
except ImportError as e:
    st.error(f"Error importing query module: {e}")
    st.stop()

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .answer-box {
        background-color: #E8F5E9;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #2E7D32;
        font-size: 1.2rem;
        line-height: 1.8;
        margin: 1rem 0;
        color: #000000;
    }
    .weather-box {
        background-color: #E3F2FD;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
    }
    .source-box {
        background-color: #FFF3E0;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
    }
    .big-font {
        font-size: 1.3rem !important;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'qa_system' not in st.session_state:
    with st.spinner("🌱 Loading AgriAssist system..."):
        try:
            st.session_state.qa_system = AgriAssistQuery()
            st.session_state.system_ready = True
        except Exception as e:
            st.error(f"Error loading system: {e}")
            st.code(str(e))
            st.session_state.system_ready = False

if 'qa_history' not in st.session_state:
    st.session_state.qa_history = []

# Header
st.markdown('<h1 class="main-header">🌾 AgriAssist</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Crop Q&A from Government PDFs & Weather Data</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    location = st.text_input(
        "📍 Location (for weather)",
        value="Delhi",
        help="Enter your city name"
    )
    
    include_weather = st.checkbox(
        "Include weather data",
        value=True,
        help="Show current weather conditions with answer"
    )
    
    st.markdown("---")
    
    st.header("📚 About")
    st.info("""
    **AgriAssist** helps farmers get answers to agricultural queries using:
    - Government agricultural PDFs
    - Real-time weather data
    - AI-powered search and answers
    
    Ask questions about crops, seasons, pests, fertilizers, and more!
    """)
    
    st.markdown("---")
    
    # Sample questions
    st.header("💡 Sample Questions")
    sample_questions = [
        "What crops are suitable for monsoon?",
        "How to control pests in wheat?",
        "Best fertilizer for rice cultivation?",
        "When to sow cotton seeds?",
        "Irrigation schedule for vegetables?",
        "Post-harvest storage methods?",
        "PM Kisan scheme details?",
        "Drip irrigation benefits?"
    ]
    
    for q in sample_questions:
        if st.button(q, key=f"sample_{q}", use_container_width=True):
            st.session_state.current_question = q
            st.rerun()

# Main content
if st.session_state.system_ready:
    
    # Question input
    col1, col2 = st.columns([4, 1])
    
    with col1:
        question = st.text_input(
            "🔍 Ask your agricultural question:",
            value=st.session_state.get('current_question', ''),
            placeholder="e.g., What is the best time to plant tomatoes?",
            key="question_input"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        ask_button = st.button("🚀 Get Answer", type="primary", use_container_width=True)
    
    # Clear the current_question after displaying
    if 'current_question' in st.session_state:
        del st.session_state.current_question
    
    # Language selector
    language = st.selectbox(
        "🌐 Language (Display)",
        ["English", "हिंदी (Hindi)", "বাংলা (Bengali)", "ਪੰਜਾਬੀ (Punjabi)", "తెలుగు (Telugu)"],
        help="Note: Core answers are in English. Translation feature for future enhancement."
    )
    
    if language != "English":
        st.info("📝 Translation feature coming soon! Currently showing results in English.")
    
    st.markdown("---")
    
    # Process query
    if ask_button and question:
        with st.spinner("🔎 Searching agricultural knowledge base and generating answer..."):
            try:
                result = st.session_state.qa_system.answer_query(
                    question,
                    location=location,
                    include_weather=include_weather
                )
                
                # Save to history
                st.session_state.qa_history.insert(0, {
                    'question': question,
                    'result': result
                })
                
                # ============ MAIN ANSWER DISPLAY ============
                st.markdown("## 📖 Your Answer")
                st.markdown(f"""
                <div class="answer-box">
                    <strong style="color: #1B5E20;">Question:</strong> <span style="color: #000;">{question}</span><br><br>
                    <strong style="color: #1B5E20;">Answer:</strong><br>
                    <span style="color: #000;">{result["answer"]}</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Display weather in columns
                if result.get('weather'):
                    st.markdown("### 🌤️ Current Weather Conditions")
                    weather = result['weather']
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("🌡️ Temperature", f"{weather['temperature']}°C")
                    with col2:
                        st.metric("💧 Humidity", f"{weather['humidity']}%")
                    with col3:
                        st.metric("☁️ Conditions", weather['description'])
                    with col4:
                        st.metric("🌧️ Rainfall", f"{weather['rainfall']}mm")
                
                # Display sources
                st.markdown("### 📚 Information Sources")
                st.info("The answer above is based on the following government documents:")
                for i, source in enumerate(result['sources'], 1):
                    st.markdown(f"**{i}.** {source}")
                
                # Success message
                st.success("✅ Answer generated successfully! You can ask another question above.")
                
                # Download button (optional)
                with st.expander("📥 Download Answer (Optional)"):
                    answer_data = {
                        'question': question,
                        'answer': result['answer'],
                        'sources': result['sources'],
                        'weather': result.get('weather'),
                        'location': result['location']
                    }
                    
                    st.download_button(
                        "Download as JSON",
                        data=json.dumps(answer_data, indent=2),
                        file_name="agriassist_answer.json",
                        mime="application/json"
                    )
                
            except Exception as e:
                st.error(f"❌ Error processing question: {e}")
                st.info("Please try rephrasing your question or check if the database was created properly.")
    
    elif not question and ask_button:
        st.warning("⚠️ Please enter a question first!")
    
    # History section
    if st.session_state.qa_history:
        st.markdown("---")
        st.markdown("## 📜 Recent Questions & Answers")
        
        with st.expander("View History", expanded=False):
            for i, item in enumerate(st.session_state.qa_history[:5], 1):
                st.markdown(f"### Q{i}: {item['question']}")
                st.markdown(f"**Answer:** {item['result']['answer']}")
                st.markdown("**Sources:**")
                for source in item['result']['sources']:
                    st.markdown(f"- {source}")
                st.markdown("---")
        
        # Clear history button
        if st.button("🗑️ Clear History"):
            st.session_state.qa_history = []
            st.rerun()

else:
    st.error("⚠️ System not ready.")
    st.info("The database should have been created automatically. If you see this message, there may be memory constraints on Streamlit Cloud.")
    
    with st.expander("📋 Deployment Tips"):
        st.markdown("""
        **For Streamlit Cloud deployment with large PDFs:**
        
        1. **Reduce PDF size**: Use only 1-2 smaller PDFs for demo
        2. **Use Git LFS**: For larger databases
        3. **Pre-build locally**: Build `db/` folder locally and upload with Git LFS
        
        **For local use:** Run `python ingest.py` first, then `streamlit run app.py`
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🌾 AgriAssist - Empowering Farmers with Knowledge</p>
    <p style='font-size: 0.8rem;'>Educational Project | Data from Government Agricultural Advisories</p>
</div>
""", unsafe_allow_html=True)