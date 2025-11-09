# 🌾 AgriAssist - Crop Q&A from Government PDFs & Weather

**An AI-powered agricultural assistant that helps farmers get answers from government agricultural PDFs combined with real-time weather data.**

---

## 📋 Project Overview

### Objective
Answer farmer queries using government agricultural PDFs and local weather data for educational purposes.

### Key Features
✅ Parse agricultural PDFs and advisories  
✅ Link weather and soil info to answers  
✅ Support for regional languages (framework ready)  
✅ Citation of sources for transparency  
✅ Real-time weather integration  
✅ User-friendly web interface  

---

## 🛠️ Tech Stack

- **LangChain**: Document processing and QA chains
- **Sentence-Transformers**: Text embeddings (all-MiniLM-L6-v2)
- **ChromaDB**: Vector database for semantic search
- **Transformers**: QA model (FLAN-T5)
- **PyPDF**: PDF parsing
- **Streamlit**: Web interface
- **Weather API**: Real-time weather data (wttr.in)

---

## 📁 Project Structure

```
agriassist/
├── data/                      # Place your PDF files here
├── db/                        # Vector database (auto-generated)
├── ingest.py                  # PDF ingestion and database creation
├── query.py                   # Query engine with weather integration
├── app.py                     # Streamlit web interface
├── sample_qa_dataset.json     # Sample Q&A pairs
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

---

## 🚀 Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Add Your PDF Documents

Place government agricultural advisory PDFs in the `data/` folder:

```bash
mkdir data
# Copy your PDF files to the data folder
```

**Recommended Sources:**
- Government agricultural department advisories
- Crop production guides
- Pest management guidelines
- Fertilizer recommendations

### 3. Create Vector Database

Run the ingestion script to process PDFs and create the searchable database:

```bash
python ingest.py
```

This will:
- Load all PDFs from `data/` folder
- Split documents into chunks
- Create embeddings
- Save vector database to `db/` folder

**Note:** You only need to run this once (or when adding new PDFs).

---

## 💻 Usage

### Method 1: Web Interface (Recommended)

Start the Streamlit app:

```bash
streamlit run app.py
```

The web interface will open in your browser with:
- Query input box
- Location selector for weather data
- Real-time weather conditions
- Answer with sources
- Sample questions
- Query history

### Method 2: Command Line

Test the query system directly:

```bash
python query.py
```

---

## 📊 Sample Q&A Dataset

The project includes 20 pre-generated Q&A pairs covering:
- **Crops**: Suitable crops for different seasons
- **Pests**: Disease identification and control
- **Fertilizers**: Nutrient management
- **Irrigation**: Water requirements
- **Weather**: Climate-based recommendations
- **Seasons**: Planting and harvesting times

View: `sample_qa_dataset.json`

---

## 🌐 Features Breakdown

### 1. Document Search
- Semantic search using embeddings
- Retrieves top 3 most relevant document chunks
- Provides source citations (document name + page)

### 2. Weather Integration
- Real-time weather from wttr.in API
- Shows temperature, humidity, conditions, rainfall
- Location-based data
- Weather-aware recommendations

### 3. AI-Powered Answers
- Uses FLAN-T5 for answer generation
- Combines document context + weather data
- Natural language responses
- Educational and practical advice

### 4. Web Interface
- Clean, farmer-friendly design
- Sample questions for guidance
- Query history tracking
- Download answers as JSON
- Multi-language display (framework ready)

---

## 📈 Impact & Use Cases

### Educational Value
- Helps students understand AI applications in agriculture
- Demonstrates RAG (Retrieval Augmented Generation)
- Shows integration of multiple data sources

### Practical Applications
- Quick access to agricultural knowledge
- Weather-aware farming advice
- 24/7 availability
- Reduces dependency on extension officers

### Target Users
- Farmers seeking crop guidance
- Agricultural students
- Extension workers
- Rural development organizations

---

## ⚠️ Limitations & Disclaimers

### Current Limitations
1. **Language**: Currently English only (translation framework ready)
2. **Data Quality**: Depends on PDF content and quality
3. **Weather API**: Free tier with usage limits
4. **Model Size**: Uses smaller models for faster inference
5. **No Voice**: Text-based interface only
6. **Offline**: Requires internet for weather data

### Important Notes
- ⚠️ **Educational Project**: Not a replacement for professional agricultural advice
- ⚠️ **Verify Information**: Always cross-check critical farming decisions
- ⚠️ **Regional Variation**: Recommendations may vary by location
- ⚠️ **Data Currency**: Ensure PDFs contain up-to-date information

---

## 🔮 Future Enhancements

### Planned Features
- [ ] Regional language support (Hindi, Bengali, Tamil, Telugu, etc.)
- [ ] Voice input/output for illiterate farmers
- [ ] Image-based crop disease detection
- [ ] Real-time market price integration
- [ ] Soil testing recommendations
- [ ] Crop calendar and reminders
- [ ] Community forum for farmers
- [ ] Mobile app (Android/iOS)

### Technical Improvements
- [ ] Larger language models for better answers
- [ ] Fine-tuning on agricultural domain
- [ ] Multi-modal inputs (text + image)
- [ ] Caching for faster responses
- [ ] User feedback mechanism
- [ ] Analytics dashboard

---

## 📚 Data Sources

### Recommended Government Sources
- **India Meteorological Department (IMD)**: Weather data
- **State Agricultural Departments**: Crop advisories
- **ICAR Institutes**: Research publications
- **Krishi Vigyan Kendras (KVK)**: Extension materials
- **Ministry of Agriculture**: Policy documents

### Citation
All answers include source citations to maintain transparency and allow users to verify information.

---

## 🤝 Contributing

This is an educational project. Suggestions for improvements:
1. Better PDF sources
2. Enhanced language support
3. Improved UI/UX
4. Additional features

---

## 📝 Sample Queries to Try

1. "What crops are suitable for monsoon season?"
2. "How to control pests in wheat crops?"
3. "Best fertilizer for rice cultivation?"
4. "When to sow cotton seeds?"
5. "Irrigation schedule for vegetables?"
6. "What to do if rainfall is delayed?"
7. "Organic pest control methods?"
8. "Benefits of intercropping?"
9. "How to increase wheat yield?"
10. "Drip irrigation advantages?"

---

## 🎓 Academic Context

### Learning Outcomes
- Understanding of RAG systems
- PDF processing and chunking strategies
- Vector databases and semantic search
- API integration (weather)
- Full-stack AI application development
- User interface design for rural users

### Technologies Demonstrated
- Natural Language Processing (NLP)
- Information Retrieval
- Text Embeddings
- Question Answering
- Web Development
- API Integration

---

## 📄 License

Educational project - feel free to use and modify for learning purposes.

---

## 👨‍💻 Quick Start Checklist

- [ ] Install Python 3.8+
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Create `data/` folder
- [ ] Add agricultural PDF files to `data/`
- [ ] Run: `python ingest.py`
- [ ] Start app: `streamlit run app.py`
- [ ] Test with sample questions
- [ ] Review generated answers and sources

---

## 🐛 Troubleshooting

### Database not found error
**Solution**: Run `python ingest.py` first

### No PDFs found error
**Solution**: Add PDF files to `data/` folder

### Weather API not working
**Solution**: Check internet connection or disable weather in settings

### Out of memory error
**Solution**: Reduce `chunk_size` in ingest.py or use smaller PDFs

### Slow performance
**Solution**: First-time model downloads take time; subsequent runs are faster

---

## 📞 Contact & Support

For academic queries or suggestions, create an issue or contact your project supervisor.

---

**Built with ❤️ for Indian Farmers**

*Empowering Agriculture through Technology*