# 🌤️ Personalized Weather Bot with LLM, LangChain & LangGraph

This project is a **smart, interactive weather chatbot** built using **LLM, LangChain, and LangGraph**. Unlike a standard website calling a weather API, this bot can understand **natural language queries**, extract the location intelligently, handle **ZIP codes, coordinates, short city forms**, and provide **personalized weather responses**.

---

## 🚀 Features

* **Natural Language Understanding**: Users can type queries like:

  * `"What’s the weather in NYC?"`
  * `"Temperature at 10001"`
  * `"Weather near Eiffel Tower"`
  * `"Current weather at 40.7128, -74.0060"`

* **LLM-powered Location Extraction**: The bot uses an LLM to detect locations from messy or ambiguous queries.

* **Generalized Weather Fetching**: Handles:

  * City names and aliases (e.g., NYC → New York)
  * ZIP/postal codes
  * Coordinates (lat, lon)
  * Landmarks

* **Caching**:

  * In-memory cache for faster responses
  * Database cache for persistence

* **Personalized Responses**: The LLM formats weather data into **human-friendly, conversational answers**.

* **Extensible Architecture**: Built using **LangGraph** for workflow management:

  * `extract_location` → `check_cache` → `fetch_from_api` → `format_answer`

---

## 🛠️ Tech Stack

| Component              | Technology / Library             |
| ---------------------- | -------------------------------- |
| LLM / Natural Language | OpenAI GPT / LangChain           |
| Workflow Orchestration | LangGraph                        |
| Weather Data API       | OpenWeather (Current + Forecast) |
| Cache                  | In-memory + Database             |
| Logging                | Python logging                   |
| Environment Variables  | dotenv                           |
| Language               | Python 3.11+                     |

---

## ⚡ How It Works

1. **User Query** → User types a question in natural language.
2. **LLM Location Extraction** → The LLM identifies the location from the query.
3. **Cache Check** → LangGraph checks in-memory and DB cache for recent weather.
4. **API Fetch (if needed)** → If no valid cache, fetch weather via OpenWeather using **coordinates**, resolving city names, ZIP codes, or landmarks.
5. **LLM Response Formatting** → The bot generates a **personalized, human-readable weather summary**.

> Unlike normal websites, this bot does not just fetch raw JSON from the API—it **understands your query**, **resolves ambiguous locations**, and **talks to you naturally**.

---

## 🏗️ Project Structure

```
weather-bot/
│
├─ orchestrator/          # LangGraph state manager
├─ tools/
│   ├─ location_resolver.py   # Extracts location from query
│   └─ weather_api.py         # Generalized weather fetch
├─ database/
│   ├─ cache.py               # DB cache utilities
├─ utils/
│   ├─ logger.py              # Logging setup
│   └─ LLM_init.py            # Initialize LLM / LangChain
├─ Schema/
│   └─ model.py               # WeatherState definition
├─ main.py                    # CLI / bot entry point
├─ requirements.txt           # Python dependencies
└─ README.md
```

---

## 🔧 Installation

1. Clone the repo:

```bash
git clone https://github.com/USERNAME/REPO_NAME.git
cd REPO_NAME
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate       # Linux / macOS
venv\Scripts\activate        # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set environment variables in `.env`:

```
OPENWEATHER_API_KEY=your_api_key_here
```

5. Run the bot:

```bash
python main.py
```

Type your query (e.g., `"Weather in San Francisco"`) and get a personalized response.

---

## 💡 Example Usage

```
Ask about the weather (or 'quit'): What's the weather in NYC?
🤖: Currently in New York, it's 22°C with light clouds. Humidity is 60% and wind speed is 10 km/h.

Ask about the weather (or 'quit'): Temperature at 10001
🤖: At ZIP code 10001, the temperature is 23°C, partly sunny.

Ask about the weather (or 'quit'): Weather near Eiffel Tower
🤖: Around the Eiffel Tower in Paris, the current weather is 18°C with scattered clouds.
```

---

## 🔄 How It Differs From a Normal API Call

* **Normal websites**: User inputs city → API returns raw JSON → User reads it.
* ** bot**:

  * Understands freeform queries using **LLM**
  * Resolves ambiguous inputs, ZIP codes, coordinates, or landmarks
  * Generates a **conversational, personalized response**
  * Caches results intelligently for faster response

---

## 📈 Extensibility

* Add **5-day forecast** by using the OpenWeather 5-day API.
* Integrate additional LLM capabilities, e.g., **clothing suggestions**, **air quality info**, **personalized notifications**.
* Deploy as **web app, Telegram/Discord bot, or voice assistant**.

---
