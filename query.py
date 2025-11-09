# query.py
import os
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from transformers import pipeline
import requests

DB_DIRECTORY = "db"

class AgriAssistQuery:
    def __init__(self):
        """Initialize the query system"""
        print("Loading AgriAssist system...")
        
        # Load embeddings
        self.embedding_model = SentenceTransformerEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Load vector database
        if not os.path.exists(DB_DIRECTORY):
            raise FileNotFoundError(
                f"Database not found at '{DB_DIRECTORY}'. "
                "Please run ingest.py first."
            )
        
        self.db = Chroma(
            persist_directory=DB_DIRECTORY,
            embedding_function=self.embedding_model
        )
        
        print("✓ Vector database loaded")
        
        # Initialize simple QA pipeline
        self.qa_pipeline = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",
            max_length=512,
            device=-1  # CPU
        )
        
        print("✓ QA model loaded")
    
    def get_weather(self, city="Delhi"):
        """Get weather data from OpenWeatherMap API"""
        try:
            # Free API - no key needed for basic data
            url = f"https://wttr.in/{city}?format=j1"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                current = data['current_condition'][0]
                weather_info = {
                    'temperature': current['temp_C'],
                    'humidity': current['humidity'],
                    'description': current['weatherDesc'][0]['value'],
                    'rainfall': current.get('precipMM', '0')
                }
                return weather_info
            else:
                return None
        except Exception as e:
            print(f"Weather API error: {e}")
            return None
    
    def search_documents(self, query, k=3):
        """Search relevant documents"""
        results = self.db.similarity_search_with_score(query, k=k)
        return results
    
    def answer_query(self, question, location="Delhi", include_weather=True):
        """Answer farmer query with context and weather"""
        
        # Search relevant documents
        search_results = self.search_documents(question)
        
        # Prepare context from documents
        context_parts = []
        sources = []
        
        for i, (doc, score) in enumerate(search_results, 1):
            context_parts.append(f"Context {i}: {doc.page_content}")
            source = doc.metadata.get('source', 'Unknown')
            sources.append(f"Document: {os.path.basename(source)}, Page: {doc.metadata.get('page', 'N/A')}")
        
        context = "\n\n".join(context_parts)
        
        # Get weather if requested
        weather_info = None
        weather_context = ""
        
        if include_weather:
            weather_info = self.get_weather(location)
            if weather_info:
                weather_context = f"\n\nCurrent Weather in {location}:\n"
                weather_context += f"Temperature: {weather_info['temperature']}°C\n"
                weather_context += f"Humidity: {weather_info['humidity']}%\n"
                weather_context += f"Conditions: {weather_info['description']}\n"
                weather_context += f"Rainfall: {weather_info['rainfall']}mm"
        
        # Generate answer
        prompt = f"""Based on the following agricultural information, answer the farmer's question clearly and practically.

{context}
{weather_context}

Question: {question}

Answer:"""
        
        answer = self.qa_pipeline(prompt, max_length=300)[0]['generated_text']
        
        return {
            'answer': answer,
            'sources': sources,
            'weather': weather_info,
            'location': location
        }

# Test function
if __name__ == "__main__":
    qa_system = AgriAssistQuery()
    
    # Test query
    result = qa_system.answer_query(
        "What crops are suitable for monsoon season?",
        location="Delhi"
    )
    
    print("\n" + "="*60)
    print("ANSWER:", result['answer'])
    print("\n" + "="*60)
    print("SOURCES:")
    for source in result['sources']:
        print(f"  • {source}")
    
    if result['weather']:
        print("\n" + "="*60)
        print(f"WEATHER IN {result['location']}:")
        print(f"  • Temperature: {result['weather']['temperature']}°C")
        print(f"  • Humidity: {result['weather']['humidity']}%")
        print(f"  • Conditions: {result['weather']['description']}")