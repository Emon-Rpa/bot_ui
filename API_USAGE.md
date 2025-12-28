# API Usage Guide

This document explains how to send data to the Message Viewer API.

## API Endpoint

**URL:** `http://localhost:5000/api/messages`

## Methods

### GET - Retrieve Messages
Retrieve the current message data.

**Request:**
```bash
curl http://localhost:5000/api/messages
```

**Response:**
```json
{
  "Title": "কাঠ গোলাপ",
  "Sub_Title": "ঢাকা বিভাগের পাত্রী পাত্র",
  "messages": [...]
}
```

---

### POST - Send New Data
Send new message data to replace the current data.

## Required JSON Format

Your JSON data must follow this structure:

```json
{
  "Title": "Your Title",
  "Sub_Title": "Your Subtitle (optional)",
  "messages": [
    {
      "user_name": "User Name",
      "user_profile_pic": "https://example.com/avatar.jpg",
      "text": "Message text content",
      "media": ["https://example.com/image1.jpg"],
      "timestamp": "2025-12-12 19:50:00",
      "reactions": {
        "👍": 5,
        "❤": 3
      }
    }
  ]
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `Title` | string | ✅ Yes | Main title of the message group |
| `Sub_Title` | string | ❌ No | Subtitle or description |
| `messages` | array | ✅ Yes | Array of message objects |
| `messages[].user_name` | string | ✅ Yes | Name of the user |
| `messages[].user_profile_pic` | string | ❌ No | URL to user's profile picture |
| `messages[].text` | string | ❌ No | Message text content |
| `messages[].media` | array | ❌ No | Array of media URLs (images) |
| `messages[].timestamp` | string | ❌ No | Timestamp in any readable format |
| `messages[].reactions` | object | ❌ No | Emoji reactions with counts |

---

## Examples

### Using cURL

```bash
curl -X POST http://localhost:5000/api/messages \
  -H "Content-Type: application/json" \
  -d '{
    "Title": "Test Messages",
    "Sub_Title": "API Test",
    "messages": [
      {
        "user_name": "John Doe",
        "user_profile_pic": "https://via.placeholder.com/100",
        "text": "Hello from API!",
        "media": [],
        "timestamp": "2025-12-12 20:00:00",
        "reactions": {"👍": 5}
      }
    ]
  }'
```

### Using Python (requests library)

```python
import requests

url = 'http://localhost:5000/api/messages'

data = {
    "Title": "Test Messages",
    "Sub_Title": "API Test",
    "messages": [
        {
            "user_name": "John Doe",
            "user_profile_pic": "https://via.placeholder.com/100",
            "text": "Hello from API!",
            "media": [],
            "timestamp": "2025-12-12 20:00:00",
            "reactions": {"👍": 5}
        }
    ]
}

response = requests.post(url, json=data)
print(response.json())
```

### Using JavaScript (fetch)

```javascript
const url = 'http://localhost:5000/api/messages';

const data = {
  Title: "Test Messages",
  Sub_Title: "API Test",
  messages: [
    {
      user_name: "John Doe",
      user_profile_pic: "https://via.placeholder.com/100",
      text: "Hello from API!",
      media: [],
      timestamp: "2025-12-12 20:00:00",
      reactions: {"👍": 5}
    }
  ]
};

fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(data)
})
.then(response => response.json())
.then(result => console.log(result))
.catch(error => console.error('Error:', error));
```

---

## Response Format

### Success Response (200)
```json
{
  "success": true,
  "message": "Data saved successfully",
  "message_count": 2
}
```

### Error Responses

**400 - Bad Request (No data)**
```json
{
  "error": "No JSON data provided"
}
```

**400 - Bad Request (Invalid format)**
```json
{
  "error": "Invalid format. Required fields: Title, messages"
}
```

**500 - Server Error**
```json
{
  "error": "Server error: [error details]"
}
```

---

## Testing the API

1. **Start the server:**
   ```bash
   cd bot_ui
   ./venv/bin/python app.py
   ```

2. **Run the example script:**
   ```bash
   ./venv/bin/python send_data_example.py
   ```

3. **Refresh your browser** at http://localhost:5000 to see the updated data

---

## Notes

- The API accepts **UTF-8 encoded** JSON, so Bengali and other Unicode characters are fully supported
- When you POST new data, it **replaces** the entire JSON file
- The UI will automatically reload and display the new data when you refresh the page
- For production use, consider adding authentication and validation
