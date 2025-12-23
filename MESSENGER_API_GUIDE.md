# Messenger API Usage Guide - New Channel/Group Structure

## Overview

The messenger API now uses a nested channel/group structure where:
- **Channel**: Identified by `author_id` (e.g., a Facebook page/profile)
- **Group**: Identified by `source` URL (e.g., a specific messenger conversation)

## Sending Messages via API

### Endpoint
```
POST http://localhost:5000/api/messages?platform=messenger
```

### Required Fields
- `author_id`: The Facebook profile/page ID
- `author_url`: The Facebook profile/page URL
- `source`: The messenger conversation URL
- `Title`: The channel/group name
- `Sub_Title`: Description (e.g., "Channel · 53.2K members")
- `icon`: **Group icon URL** (also used as the channel icon)
- `messages`: Array of message objects

> **Note:** The `icon` field represents the group's icon. When creating a new channel, this icon is also used as the channel icon. If adding a new group to an existing channel, the icon will update the channel icon if provided.

### Example Request (Python)

```python
import requests
import json

url = "http://localhost:5000/api/messages?platform=messenger"

data = {
    "author_id": "166064673583399",
    "author_url": "https://www.facebook.com/profile.php?id=166064673583399",
    "source": "https://www.messenger.com/t/9326713427339811",
    "Title": "Bangladesh Awami League",
    "Sub_Title": "Channel\n  · 53.2K members",
    "icon": "https://scontent.fdac31-1.fna.fbcdn.net/v/t1.15752-9/462581636_1502069793810508_6755015222113481180_n.jpg",
    "messages": [
        {
            "user_name": "Bangladesh Awami League",
            "user_profile_pic": "https://scontent.fdac31-2.fna.fbcdn.net/v/t39.30808-1/487923508_1118206017002346_7869138773571212541_n.jpg",
            "text": "https://www.facebook.com/share/v/17nkCnigC4/?mibextid=wwXIfr",
            "media": [
                "https://scontent.fdac31-2.fna.fbcdn.net/v/t39.30808-1/487923508_1118206017002346_7869138773571212541_n.jpg"
            ],
            "timestamp": "2025-12-21 22:09:00",
            "reactions": {
                "👍": 69,
                "❤": 23,
                "😢": 6
            }
        }
    ]
}

response = requests.post(url, json=data)
print(response.json())
```

### Example Request (cURL)

```bash
curl -X POST http://localhost:5000/api/messages?platform=messenger \
  -H "Content-Type: application/json" \
  -d '{
    "author_id": "166064673583399",
    "author_url": "https://www.facebook.com/profile.php?id=166064673583399",
    "source": "https://www.messenger.com/t/9326713427339811",
    "Title": "Bangladesh Awami League",
    "Sub_Title": "Channel · 53.2K members",
    "icon": "https://example.com/icon.jpg",
    "messages": [
      {
        "user_name": "User Name",
        "user_profile_pic": "https://example.com/avatar.jpg",
        "text": "Message text",
        "media": [],
        "timestamp": "2025-12-21 22:09:00",
        "reactions": {"👍": 10}
      }
    ]
  }'
```

### Success Response

```json
{
  "success": true,
  "platform": "messenger",
  "author_id": "166064673583399",
  "source": "https://www.messenger.com/t/9326713427339811",
  "title": "Bangladesh Awami League",
  "total_messages_sent": 1,
  "messages_added": 1,
  "duplicates_skipped": 0,
  "channel_action": "created",
  "group_action": "created"
}
```

## How It Works

1. **First Request**: Creates both channel and group
   - `channel_action: "created"`
   - `group_action: "created"`

2. **Same Channel, New Group**: Adds group to existing channel
   - `channel_action: "updated"`
   - `group_action: "created"`

3. **Same Channel & Group**: Appends messages to existing group
   - `channel_action: "updated"`
   - `group_action: "updated"`
   - Duplicate messages are automatically skipped

## Duplicate Detection

Messages are considered duplicates if they have the same:
- `user_name`
- `text`
- `timestamp`

## Retrieving Messages

### Get All Channels
```
GET http://localhost:5000/api/groups?platform=messenger
```

### Get Specific Group Messages
```
GET http://localhost:5000/api/messages?platform=messenger&author_id=166064673583399&source=https://www.messenger.com/t/9326713427339811
```
