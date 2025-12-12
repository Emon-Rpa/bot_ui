# WhatsApp API Usage Guide - Postman

Quick guide for sending WhatsApp channel data to the API using Postman.

## API Endpoint

**URL:** `http://localhost:5000/api/messages?platform=whatsapp`  
**Method:** `POST`  
**Content-Type:** `application/json`

## Required JSON Format

```json
{
  "Source_name": "Channel Name",
  "Source_link": "https://whatsapp.com/channel/...",
  "Followers": "1000",
  "Profile_picture": "https://example.com/profile.jpg",
  "posts": [
    {
      "Post_text": "Your post text here",
      "Post_image": "https://example.com/image.jpg",
      "Post_time": "8:55 PM",
      "Post_reaction": "52",
      "Post_scraping_time": "2025-12-13 01:00:00"
    }
  ]
}
```

## Postman Setup Steps

### 1. Create New Request
- Click **New** → **HTTP Request**
- Set method to **POST**
- Enter URL: `http://localhost:5000/api/messages?platform=whatsapp`

### 2. Set Headers
Go to **Headers** tab and add:
```
Key: Content-Type
Value: application/json
```

### 3. Set Body
Go to **Body** tab:
- Select **raw**
- Choose **JSON** from dropdown
- Paste your JSON data

### 4. Example Request Body

```json
{
  "Source_name": "Test Channel",
  "Source_link": "https://whatsapp.com/channel/test",
  "Followers": "5000",
  "Profile_picture": "https://via.placeholder.com/100",
  "posts": [
    {
      "Post_text": "This is a test post from Postman!",
      "Post_image": "https://via.placeholder.com/300",
      "Post_time": "1:00 PM",
      "Post_reaction": "10",
      "Post_scraping_time": "2025-12-13 01:00:00"
    },
    {
      "Post_text": "Another test post with Bengali text: হ্যালো!",
      "Post_image": "https://via.placeholder.com/300",
      "Post_time": "2:00 PM",
      "Post_reaction": "25",
      "Post_scraping_time": "2025-12-13 02:00:00"
    }
  ]
}
```

### 5. Send Request
Click **Send** button

## Expected Response

### Success (200 OK)
```json
{
  "success": true,
  "platform": "whatsapp",
  "source_name": "Test Channel",
  "post_count": 2,
  "action": "created"
}
```

### Error (400 Bad Request)
```json
{
  "error": "Invalid format. Required: Source_name, posts"
}
```

## Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `Source_name` | string | ✅ Yes | Channel name (unique identifier) |
| `Source_link` | string | ❌ No | WhatsApp channel URL |
| `Followers` | string | ❌ No | Follower count |
| `Profile_picture` | string | ❌ No | Channel profile picture URL |
| `posts` | array | ✅ Yes | Array of post objects |
| `posts[].Post_text` | string | ❌ No | Post text content |
| `posts[].Post_image` | string | ❌ No | Post image URL |
| `posts[].Post_time` | string | ❌ No | Post time |
| `posts[].Post_reaction` | string | ❌ No | Reaction count |
| `posts[].Post_scraping_time` | string | ❌ No | When post was scraped |

## Important Notes

1. **Unique Identifier:** `Source_name` is used as the unique identifier
   - If a channel with the same name exists, it will be **updated**
   - If it's new, it will be **created** at the top of the list

2. **Bengali Text:** Fully supported - just paste Bengali text directly

3. **Image URLs:** Can be local paths or remote URLs
   - Local: `post_screenshots/image.png`
   - Remote: `https://example.com/image.jpg`

4. **Optional Fields:** All fields except `Source_name` and `posts` are optional

## Quick Test in Postman

Copy this minimal example to test quickly:

```json
{
  "Source_name": "My Test Channel",
  "posts": [
    {
      "Post_text": "Hello from Postman!",
      "Post_time": "Now"
    }
  ]
}
```

After sending, refresh your browser at `http://localhost:5000` and:
1. Click the **WhatsApp** tab
2. You should see "My Test Channel" in the sidebar
3. Click it to view the post

## Updating Existing Channel

To add more posts to an existing channel, send the **complete** data including all posts:

```json
{
  "Source_name": "Jamuna Television",
  "Source_link": "https://whatsapp.com/channel/0029VakgKm5LdQeemosdqc0F",
  "Followers": "182,083",
  "Profile_picture": "https://...",
  "posts": [
    {
      "Post_text": "New post 1",
      "Post_time": "3:00 PM"
    },
    {
      "Post_text": "New post 2",
      "Post_time": "4:00 PM"
    }
  ]
}
```

This will **replace** all existing posts for that channel.

## Troubleshooting

**Error: Connection refused**
- Make sure Flask server is running: `./venv/bin/python app.py`

**Error: Invalid JSON**
- Check for missing commas, quotes, or brackets
- Use Postman's JSON validator (it highlights errors)

**Channel not appearing**
- Refresh the browser
- Check the response - it should say `"success": true`
- Verify the platform parameter: `?platform=whatsapp`

**Bengali text showing as ???**
- Make sure Content-Type is `application/json`
- Postman should handle UTF-8 automatically
