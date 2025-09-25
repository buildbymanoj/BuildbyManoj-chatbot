# BuildbyManoj Chatbot

Link: [https://buildbymanoj-chatbot.onrender.com](https://buildbymanoj-chatbot.onrender.com)

A modern, responsive web-based chatbot with **session management** and **RAG** (Retrieval-Augmented Generation) capabilities. This Flask-powered AI assistant uses OpenRouter's DeepSeek-V3 model and scrapes DuckDuckGo for real-time information.

## Features

- **Session-Based Memory**: The chatbot remembers your entire conversation during a browser session
- **RAG (Retrieval-Augmented Generation)**: Automatically searches the web for real-time information when needed
- **Responsive UI**: Clean, modern interface that works on both desktop and mobile devices
- **Markdown Support**: Bot responses support markdown formatting for better readability
- **Smart Web Search**: Intelligently decides when to use web search based on the query

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **AI**: DeepSeek Chat model via OpenRouter API
- **Web Scraping**: BeautifulSoup4 for DuckDuckGo search results
- **Session Management**: Flask-Session for browser session-based conversation history

## Getting Started

### Prerequisites

- Python 3.7+
- OpenRouter API key

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/buildbymanoj/BuildbyManoj-chatbot.git
   cd BuildbyManoj-chatbot
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your API key:
   ```
   OPENROUTER_API_KEY=your_api_key_here
   ```

4. Run the application:
   ```
   python app1.py
   ```

5. Open your browser and navigate to `http://localhost:10000`

## How It Works

1. **User Input**: User sends a message through the web interface
2. **RAG Decision**: System decides whether web search is needed based on keywords and query complexity
3. **Web Search**: If needed, retrieves relevant information from DuckDuckGo
4. **API Call**: Sends user message, web search results (if any), and conversation history to the AI
5. **Response**: AI generates a response which is displayed to the user
6. **Session Storage**: Both the user message and AI response are stored in the session for context

## Deployment

The app is already deployed on Render.com and includes a `render.yaml` file for easy deployment.

## License

This project is open-source and available for personal and commercial use.

## Credits

Developed by BuildbyManoj
