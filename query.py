import os
import requests
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

DB_DIRECTORY = "db"

# Weather code → human readable description
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Light rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    95: "Thunderstorm",
}

class AgriAssistQuery:
    def __init__(self):
        print("🌱 Loading AgriAssist (Gemini 2.5 Pro Edition)...")

        # Load API key
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("❌ GEMINI_API_KEY not found. Add it to your .env file.")

        # Init Gemini
        genai.configure(api_key=api_key)

        # Load Gemini 2.5 Pro model
        self.model = genai.GenerativeModel("models/gemini-2.5-pro")

        # Load embeddings
        self.embedding_model = SentenceTransformerEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )

        # Ensure DB exists
        if not os.path.exists(DB_DIRECTORY):
            raise FileNotFoundError(
                f"❌ DB folder not found at '{DB_DIRECTORY}'. Run ingest.py first."
            )

        # Load Chroma vector DB
        self.db = Chroma(
            persist_directory=DB_DIRECTORY,
            embedding_function=self.embedding_model
        )

        print("✅ Vector DB Loaded")
        print("✅ Gemini 2.5 Pro Ready")

    # -----------------------------------------------------------
    # 🌧️ OPEN-METEO WEATHER (SAFE + RELIABLE)
    # -----------------------------------------------------------
    def get_weather(self, city="Delhi"):
        try:
            # Step 1: Convert city to latitude & longitude
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
            g = requests.get(geo_url, timeout=10).json()

            if "results" not in g or len(g["results"]) == 0:
                print("⚠️ City not found in geocoding")
                return None

            lat = g["results"][0]["latitude"]
            lon = g["results"][0]["longitude"]

            # Step 2: Fetch weather
            weather_url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat}&longitude={lon}&current_weather=true"
            )

            w = requests.get(weather_url, timeout=10).json()

            if "current_weather" not in w:
                return None

            cw = w["current_weather"]
            wcode = cw.get("weathercode", 0)

            return {
                "temperature": cw.get("temperature", "N/A"),
                "humidity": "N/A",
                "description": WEATHER_CODES.get(wcode, "Not available"),
                "rainfall": cw.get("rain", 0),
            }

        except Exception as e:
            print(f"⚠️ Weather API error: {e}")
            return None

    # -----------------------------------------------------------
    # 🔍 VECTOR SEARCH
    # -----------------------------------------------------------
    def search_documents(self, query, k=3):
        return self.db.similarity_search_with_score(query, k=k)

    # -----------------------------------------------------------
    # 🤖 MAIN RAG PIPELINE — Gemini 2.5 Pro
    # -----------------------------------------------------------
    def answer_query(self, question, location="Delhi", include_weather=True):

        # 1. Retrieve PDF context
        results = self.search_documents(question)

        context_blocks = []
        sources = []

        for i, (doc, score) in enumerate(results, 1):
            context_blocks.append(
                f"Source {i}:\n{doc.page_content.strip()}\n"
            )
            src = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page", "N/A")
            sources.append(f"{os.path.basename(src)} — Page {page}")

        context_text = "\n\n".join(context_blocks)

        # 2. Weather context
        weather_info = None
        weather_text = ""

        if include_weather:
            weather_info = self.get_weather(location)
            if weather_info:
                weather_text = (
                    f"\nCurrent Weather in {location}:\n"
                    f"- Temperature: {weather_info['temperature']}°C\n"
                    f"- Humidity: {weather_info['humidity']}%\n"
                    f"- Condition: {weather_info['description']}\n"
                    f"- Rainfall: {weather_info['rainfall']}mm\n"
                )

        # 3. Build prompt
        prompt = f"""
You are AgriAssist, an agricultural expert for Indian farmers.
Provide clear, practical, and reliable guidance based ONLY on the given PDF context and weather.

-------------------------
📘 PDF CONTEXT:
{context_text}

-------------------------
🌦 WEATHER CONTEXT:
{weather_text}

-------------------------
❓ FARMER'S QUESTION:
{question}

-------------------------
✍️ FINAL ANSWER (Simple, Practical, Beginner-Friendly):
"""

        # 4. Generate answer using Gemini 2.5 Pro
        try:
            response = self.model.generate_content([prompt])
            answer = response.text.strip()
        except Exception as e:
            print(f"⚠️ Gemini Error: {e}")
            answer = "The system could not generate an answer. Please try again."

        return {
            "answer": answer,
            "sources": sources,
            "weather": weather_info,
            "location": location,
        }

# Test Mode
if __name__ == "__main__":
    bot = AgriAssistQuery()
    res = bot.answer_query("What crops are suitable for monsoon?")
    print(res["answer"])
    
    
    
    
    