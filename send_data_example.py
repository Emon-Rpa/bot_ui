#!/usr/bin/env python3
"""
Example script showing how to send data to the Message Viewer API
"""

import requests
import json

# API endpoint
API_URL = 'http://localhost:5000/api/messages'

# Example data in the same format as your JSON file
example_data = {
    "Title": "Test Messages",
    "Sub_Title": "Example data sent via API",
    "messages": [
        {
            "user_name": "John Doe",
            "user_profile_pic": "https://via.placeholder.com/100",
            "text": "This is a test message sent via API!",
            "media": [],
            "timestamp": "2025-12-12 19:50:00",
            "reactions": {
                "👍": 5,
                "❤": 3
            }
        },
        {
            "user_name": "Jane Smith",
            "user_profile_pic": "https://via.placeholder.com/100",
            "text": "Another example message with Bengali text: হ্যালো!",
            "media": [
                "https://via.placeholder.com/300"
            ],
            "timestamp": "2025-12-12 19:51:00",
            "reactions": {
                "😊": 2
            }
        }
    ]
}

def send_data():
    """Send data to the API"""
    try:
        # Send POST request with JSON data
        response = requests.post(
            API_URL,
            json=example_data,
            headers={'Content-Type': 'application/json'}
        )
        
        # Check response
        if response.status_code == 200:
            print("✅ Success!")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Message: {response.json()}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to server. Make sure the Flask app is running.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def get_data():
    """Get current data from the API"""
    try:
        response = requests.get(API_URL)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Retrieved data:")
            print(f"Title: {data.get('Title')}")
            print(f"Subtitle: {data.get('Sub_Title')}")
            print(f"Number of messages: {len(data.get('messages', []))}")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    print("=== Message Viewer API Example ===\n")
    
    # First, get current data
    print("1. Getting current data...")
    get_data()
    
    print("\n" + "="*50 + "\n")
    
    # Then, send new data
    print("2. Sending new data...")
    send_data()
    
    print("\n" + "="*50 + "\n")
    
    # Get data again to verify
    print("3. Verifying updated data...")
    get_data()
