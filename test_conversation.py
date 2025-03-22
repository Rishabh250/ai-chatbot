import os
import random
import requests
import threading
import time
import uuid
from dotenv import load_dotenv
import argparse

load_dotenv()

API_URL = f"http://localhost:{os.getenv('API_PORT', '8000')}/api/chat"

def send_message(message, user_id=None):
    try:
        payload = {"message": message}
        if user_id:
            payload["user_id"] = user_id
            
        response = requests.post(
            API_URL,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return {"response": f"Error: {e}"}

def simulate_conversation(user_name, delay_factor=1.0):
    user_id = str(uuid.uuid4())
    messages = [
        f"Hello, I'm interested in your product. My name is {user_name}",
        f"You can reach me at {user_name.lower().replace(' ', '.')}@example.com",
        f"My phone number is 555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
        "I heard about you from a friend"
    ]
    
    print(f"\n=== Starting Conversation Simulation for {user_name} (ID: {user_id}) ===\n")
    
    for i, message in enumerate(messages):
        print(f"USER {user_name}: {message}")
        response = send_message(message, user_id)
        print(f"BOT -> {user_name}: {response.get('response', 'No response')}")
        if 'leadId' in response:
            print(f"\n*** Lead created for {user_name} with ID: {response['leadId']} ***\n")
        if i < len(messages) - 1:
            print("\n---\n")
            time.sleep(delay_factor * (1 + random.random()))
    
    print(f"\n=== Conversation Simulation Complete for {user_name} ===\n")
    return user_id

def simulate_multiple_conversations():
    users = [
        "John Smith",
        "Alice Johnson",
    ]
    
    threads = []
    for i, user in enumerate(users):
        delay_factor = 0.5 + (i * 0.3)
        thread = threading.Thread(target=simulate_conversation, args=(user, delay_factor))
        threads.append(thread)
    
    for thread in threads:
        thread.start()
        time.sleep(0.5)
    
    for thread in threads:
        thread.join()
    
    print("\n=== All Conversation Simulations Complete ===\n")
    
    try:
        sessions_response = requests.get(f"http://localhost:{os.getenv('API_PORT', '8000')}/api/chat/sessions")
        sessions = sessions_response.json()
        print(f"Active Sessions: {sessions['count']}")
        for session_id in sessions['active_sessions']:
            print(f"- {session_id}")
    except Exception as e:
        print(f"Error retrieving sessions: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test the chatbot API")
    parser.add_argument("--user", help="Run a single user conversation with the specified name")
    parser.add_argument("--multi", action="store_true", help="Run multiple user conversations concurrently")
    
    args = parser.parse_args()
    
    if args.user:
        simulate_conversation(args.user)
    elif args.multi:
        simulate_multiple_conversations()
    else:
        simulate_conversation("John Smith") 