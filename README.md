
#  Research Assistant Chatbot

A smart research assistant powered by **LangChain**, **Anthropic Claude 3.5**, and real-time tools like **DuckDuckGo** and **Wikipedia**. It generates structured research outputs from user queries, optionally saving them to a local file.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/Built%20with-LangChain-ef5b25)](https://www.langchain.com/)
[![Anthropic Claude](https://img.shields.io/badge/LLM-Claude%203.5-lightgrey)](https://www.anthropic.com/)

---

##  Features

* Uses **Claude 3.5 Sonnet** for natural language understanding
* Integrates **DuckDuckGo** and **Wikipedia** as tools
* Saves research results to a `.txt` file with timestamps
* Outputs responses in a structured format using **Pydantic**
* Fully extensible for more tools or UI layers

---

## 📁 Project Structure

```
.
├── chatbot.py           # Main script that executes the agent
├── tools.py             # Defines external tools (search, wiki, save)
├── .env                 # API keys for Anthropic and OpenAI
├── requirements.txt     # All required Python packages
└── research_output.txt  # (Auto-created) File for saved outputs
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/research-assistant-chatbot.git
cd research-assistant-chatbot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up API Keys

Create a `.env` file in the root directory:

```
ANTHROPIC_KEY=your_anthropic_key_here
GPT_KEY=your_openai_key_if_needed
```

> **Note:** Only the `ANTHROPIC_KEY` is used in the current version.

---

## 🧠 How It Works

### `chatbot.py`

* Loads API keys from `.env`
* Defines a structured output model using `Pydantic`
* Creates a LangChain agent with integrated tools
* Accepts a research query from the user
* Allows the LLM to decide which tools to call
* Parses the structured response and prints it
* Optionally saves the response to `research_output.txt`

### `tools.py`

* **DuckDuckGo**: Performs web searches for updated information
* **Wikipedia**: Fetches concise summaries using Wikipedia API
* **Save Tool**: Saves results to a `.txt` file with a timestamp

---

## 💡 Example

```bash
$ python chatbot.py
What can I help you research? Effects of machine learning in agriculture
```

Sample Output:

```json
{
  "topic": "Effects of machine learning in agriculture",
  "summary": "Machine learning enhances crop yield prediction, pest detection, and resource optimization in agriculture. It enables precision farming through data-driven insights.",
  "sources": [
    "https://en.wikipedia.org/wiki/Machine_learning_in_agriculture",
    "https://duckduckgo.com/?q=machine+learning+in+agriculture"
  ],
  "tools_used": ["wikipedia", "search"]
}
```

Saved in `research_output.txt` if the save tool is used.

---

## 📦 Requirements

* Python 3.10+
* `langchain`
* `langchain-openai`
* `langchain-anthropic`
* `langchain-community`
* `wikipedia`
* `duckduckgo-search`
* `pydantic`
* `python-dotenv`

Install all with:

```bash
pip install -r requirements.txt
```
