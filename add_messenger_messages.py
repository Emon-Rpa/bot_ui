#!/usr/bin/env python3
"""
Example script to add new messages to a Messenger group.
This demonstrates how to use the /api/messages endpoint with duplicate prevention.
"""

import requests
import json

# API endpoint
API_URL = "http://localhost:5000/api/messages?platform=messenger"
# For deployed version, use:
# API_URL = "https://bot-ui.onrender.com/api/messages?platform=messenger"

# Example: Adding new messages to an existing group
new_data = {
    "Title": "কাঠ গোলাপ",
    "Sub_Title": "ঢাকা  পাত্রী পাত্র",
    "messages": [
        {
            "user_name": "Test User",
            "user_profile_pic": "https://example.com/profile.jpg",
            "text": "This is a test message",
            "media": [],
            "timestamp": "2025-12-13 16:30:00",
            "reactions": {}
        },
        {
            "user_name": "Another User",
            "user_profile_pic": "https://example.com/profile2.jpg",
            "text": "Another test message",
            "media": ["https://example.com/image.jpg"],
            "timestamp": "2025-12-13 16:31:00",
            "reactions": {"❤": 2}
        }
    ]
}

def add_messages():
    """Send new messages to the API"""
    try:
        print(f"Sending {len(new_data['messages'])} messages to group: {new_data['Title']}")
        
        response = requests.post(
            API_URL,
            json=new_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Success!")
            print(f"Platform: {result.get('platform')}")
            print(f"Group: {result.get('title')}")
            print(f"Action: {result.get('action')}")
            print(f"Total messages sent: {result.get('total_messages_sent')}")
            print(f"Messages added: {result.get('messages_added')}")
            print(f"Duplicates skipped: {result.get('duplicates_skipped')}")
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(response.json())
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the server.")
        print("Make sure the Flask app is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    add_messages()
