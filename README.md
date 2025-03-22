# AI Lead Collection Chatbot

A conversational AI chatbot that extracts lead information from conversations and submits it to a lead management API. Built with FastAPI, LangChain, and Google's Gemini model.

## Architecture

The system consists of:

- **FastAPI Backend**: Handles HTTP requests and responses
- **Gemini AI Model**: Extracts lead information from natural language conversations
- **LangChain Framework**: Manages prompts and parsing of AI responses
- **Lead Client**: Submits collected lead data to an external API
- **Chat Memory**: Maintains conversation history for each user
- **Session Management**: Supports multiple concurrent users
- **Mock API**: For testing and development

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Google API key for Gemini model

## Project Setup

1. Clone the repository
   ```bash
   git clone https://github.com/Rishabh250/ai-chatbot.git
   cd ai-chatbot
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables
   ```bash
   cp .env.example .env
   ```
   
   Then edit `.env` file with your configuration:
   ```
   # API configuration
   API_HOST=0.0.0.0
   API_PORT=8000

   # Google API
   GOOGLE_API_KEY=your_google_api_key_here

   # External API endpoints
   BASE_API=http://localhost:8001/api
   ```

## Running the Application

### Step 1: Start the Mock API Server

The mock API simulates an external lead management system:

```bash
python mock_api.py
```

This runs on port 8001 by default and provides these endpoints:
- `POST /api/admin/lead` - Create a new lead

### Step 2: Start the Chatbot API

```bash
python -m app.main
```

This runs on port 8000 by default and provides:
- `POST /api/chat` - Send messages to the chatbot
- `GET /api/chat/sessions` - List active user sessions
- `GET /api/chat/history/{user_id}` - Get conversation history for a user
- `DELETE /api/chat/session/{user_id}` - Clear a user's session

### Step 3: Test the Conversation Flow

To test the system with a simulated conversation:

```bash
# Test with a single user
python test_conversation.py

# Test with a specific user name
python test_conversation.py --user "Jane Doe"

# Test multiple concurrent users
python test_conversation.py --multi
```

## Multi-User Support

The system supports multiple concurrent users with the following features:

1. **User Identification**: Each user is assigned a unique ID (either provided or generated)
2. **Session Management**: Separate conversation contexts for each user
3. **Conversation Memory**: Each user's chat history is preserved
4. **Lead Tracking**: Lead information is collected separately for each user

### How to Use Multi-User Features

When sending requests to the API, include a `user_id` in the request body:

```json
{
  "message": "Hello, I'm interested in your service",
  "userId": "unique-user-identifier"
}
```

If no `userId` is provided, a new one will be generated and returned in the response.

## System Workflow

1. User sends a message to the `/api/chat` endpoint with their user ID
2. The system retrieves or creates a session for that user
3. The LangChain agent with Gemini model extracts relevant lead information
4. The conversation history is preserved in memory
5. The LeadDataCollector accumulates information over multiple messages
6. When all required fields are collected, data is submitted to the lead API
7. The bot responds with appropriate follow-up questions or confirmation

## Lead Information Collected

The system extracts and collects:
- Name
- Email
- Phone number
- Lead source
- Additional notes (optional)

## API Endpoints

### Chatbot API

- `GET /` - Home page and API status
- `POST /api/chat` - Chat with the bot
  - Request: `{"message": "Your message here", "userId": "optional-user-id"}`
  - Response: `{"response": "Bot response", "leadId": "ID if created", "user_id": "user-id"}`

### Session Management API

- `GET /api/chat/sessions` - List all active user sessions
- `GET /api/chat/history/{user_id}` - Get conversation history for a user
- `DELETE /api/chat/session/{user_id}` - Clear a user's session

### Mock Lead API

- `POST /api/admin/lead` - Create a new lead

## Troubleshooting

### Connection Issues

If you see errors like "Connection refused" when submitting leads:
1. Verify both APIs are running (check ports 8000 and 8001)
2. Confirm the `BASE_API` in your `.env` file is correct
3. Check for any firewall or network restrictions

### AI Model Issues

If lead extraction isn't working properly:
1. Verify your Google API key is valid and has access to Gemini models
2. Check the model compatibility in `langchain_agent.py`

## Project Structure

```
ai-chatbot/
│
├── app/                     # Main application
│   ├── models/              # Pydantic models
│   ├── routers/             # API routes
│   ├── services/            # Business logic
│   │   ├── chat_memory.py   # Chat memory and session management
│   │   ├── lead_client.py   # Lead API client
│   │   └── langchain_agent.py # AI model integration
│   └── main.py              # FastAPI application entry point
│
├── mock_api.py              # Mock lead API for testing
├── test_conversation.py     # Conversation testing script
├── requirements.txt         # Python dependencies
├── .env.example             # Example environment variables
└── README.md                # This file
```
