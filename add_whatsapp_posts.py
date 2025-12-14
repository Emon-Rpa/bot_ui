#!/usr/bin/env python3
"""
Example script to add new posts to a WhatsApp channel.
This demonstrates how to use the /api/messages endpoint with duplicate prevention.
"""

import requests
import json

# API endpoint
API_URL = "http://localhost:5000/api/messages?platform=whatsapp"
# For deployed version, use:
# API_URL = "https://bot-ui.onrender.com/api/messages?platform=whatsapp"

# Example: Adding new posts to an existing channel
new_data = {
    "Source_name": "Jamuna Television",
    "Source_link": "https://whatsapp.com/channel/0029VakgKm5LdQeemosdqc0F",
    "Followers": "182,083",
    "Profile_picture": "https://pps.whatsapp.net/m1/v/t24/An9oxUt3_i-m27mYMDsGqrMpY1vlEfPbBv6Ffh84eXMvK3tnkCs0GXU71YxEboYwnIrMZssYhu_idad0GN0UkZGgeEor-6L2ejpwU7XvY6MwtBDvwiUuBeO7zJ2z1WFdEeDuRf3UXsGACsMQChE?stp=dst-jpg_tt6&ccb=10-5&oh=01_Q5Aa3QEaBLarNxHMgBg_DfRlGmL_rjA1G-crocu34Et9zehEVw&oe=6940100B&_nc_sid=5e03e0&_nc_cat=104",
    "posts": [
        {
            "Post_text": "Test post from API",
            "Post_image": "post_screenshots/test_post_1.png",
            "Post_time": "4:30 PM",
            "Post_reaction": "5",
            "Post_scraping_time": "2025-12-13 16:30:00"
        },
        {
            "Post_text": "Another test post",
            "Post_image": "post_screenshots/test_post_2.png",
            "Post_time": "4:35 PM",
            "Post_reaction": "10",
            "Post_scraping_time": "2025-12-13 16:35:00"
        }
    ]
}

def add_posts():
    """Send new posts to the API"""
    try:
        print(f"Sending {len(new_data['posts'])} posts to channel: {new_data['Source_name']}")
        
        response = requests.post(
            API_URL,
            json=new_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Success!")
            print(f"Platform: {result.get('platform')}")
            print(f"Channel: {result.get('source_name')}")
            print(f"Action: {result.get('action')}")
            print(f"Total posts sent: {result.get('total_posts_sent')}")
            print(f"Posts added: {result.get('posts_added')}")
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
    add_posts()
