# 🌾 AgriAssist — Smart Agriculture Q&A (Gemini 2.5 Pro + RAG)

**AgriAssist is an AI-powered agricultural assistant that answers farmer queries using government agricultural PDFs + real-time weather data, powered by Gemini 2.5 Pro.**

It uses Retrieval-Augmented Generation (RAG) to pull information from your PDF notes and combine it with accurate weather conditions for smarter answers.

---

## 🚀 Features

### 🔍 RAG-Based PDF Search  
- Semantic search over government agricultural PDFs  
- Retrieves most relevant chunks with citations  

### 🤖 Gemini 2.5 Pro Answering  
- Handles long context  
- Provides clear, practical, agriculture-focused responses  

### 🌦️ Real-Time Weather (Open-Meteo)  
- Stable API (no key required)  
- Converts city → lat/lon → forecast  
- Gives temperature, conditions, rainfall  

### 🖥️ Clean Streamlit UI  
- Easy for farmers & beginners  
- Toggle weather on/off  
- Mobile-friendly design  

### 📘 Source Transparency  
- Displays PDF source name & page number  
- Perfect for viva & academic demonstration  

---

## 🛠 Tech Stack

| Component | Technology |
|----------|------------|
| LLM | **Gemini 2.5 Pro** |
| Embeddings | SentenceTransformer (all-MiniLM-L6-v2) |
| Vector DB | ChromaDB |
| Framework | Streamlit |
| Weather | Open-Meteo API |
| PDF Loader | LangChain PyPDF Loader |

---

## 📁 Project Structure

```
AgriAssist/
│── data/                 # Put all your PDF files here
│── db/                   # Auto-generated ChromaDB vector store
│── ingest.py             # PDF chunking + embedding pipeline
│── query.py              # Gemini 2.5 Pro RAG engine (with weather)
│── app.py                # Streamlit UI
│── requirements.txt
│── README.md
└── .env                  # GEMINI_API_KEY
```

---

## ⚙️ Installation Guide

### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Add your Gemini API key  
Create a `.env` file:
```
GEMINI_API_KEY=your_key_here
```

### 3️⃣ Add PDFs  
Place all agricultural PDFs inside:
```
data/
```

### 4️⃣ Build the vector database
```bash
python ingest.py
```

### 5️⃣ Run the app
```bash
streamlit run app.py
```

---

## 💡 How It Works (Architecture)

### **1. PDF Ingestion (`ingest.py`)**  
- Loads all PDFs  
- Splits into 400-char chunks  
- Embeds using MiniLM  
- Stores in ChromaDB  

### **2. Query Engine (`query.py`)**  
- Searches vector DB  
- Fetches weather via Open-Meteo  
- Builds context prompt  
- Sends to Gemini 2.5 Pro  
- Returns structured answer + citations  

### **3. Frontend (`app.py`)**  
- Clean UI for asking questions  
- Weather toggle  
- Cards for answers, weather & sources  

---

## 🧪 Sample Questions

Try asking:
- *"What crops can I grow in monsoon?"*  
- *"How to control pests in wheat?"*  
- *"Fertilizer schedule for rice?"*  
- *"Best crops for sandy soil?"*  
- *"What to do during unexpected rainfall?"*  

---

## 🔮 Future Improvements

- 🌐 Regional language support  
- 🎙️ Voice input & output  
- 🤳 Crop disease detection (image-based)  
- 💹 Market price integration  
- 📅 Crop calendar  
- 📱 Dedicated mobile app  

---

## ⚠️ Disclaimer
This is an **educational project**.  
Always verify critical farming decisions with local agricultural experts.

---

## 🤝 Contributing
PRs, issues, and suggestions are welcome!

---

### **Built with ❤️ for Indian Farmers**  
*Empowering agriculture with AI & open data.*

