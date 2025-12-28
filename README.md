# Multi-Platform Message Viewer

A modern web application for viewing and managing messages from multiple platforms (Messenger and WhatsApp) with a beautiful, responsive UI supporting Bengali text.

![Platform Support](https://img.shields.io/badge/Platforms-Messenger%20%7C%20WhatsApp-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![Flask](https://img.shields.io/badge/Flask-3.0.0-lightgrey)

## Features

- 💬 **Multi-Platform Support** - Messenger groups and WhatsApp channels
- 🎨 **Modern UI** - Dark theme with glassmorphism effects
- 🌐 **Bengali Support** - Full UTF-8 encoding with Noto Sans Bengali font
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- 🔄 **Real-time Switching** - Easy platform tabs for quick navigation
- 🎯 **Duplicate Prevention** - Uses Title/Source_name as unique identifiers
- 🚀 **RESTful API** - Clean API for data management

## Screenshots

- **Messenger View**: Message groups with user profiles, text, media, and reactions
- **WhatsApp View**: Channel posts with follower counts and reaction metrics
- **Platform Tabs**: Easy switching between Messenger and WhatsApp

## Quick Start

### 1. Install Dependencies

```bash
cd bot_ui

# Create virtual environment (if not exists)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/Mac
# OR
venv\Scripts\activate  # On Windows

# Install requirements
pip install -r requirements.txt
```

### 2. Migrate Existing Data (First Time Only)

If you have existing JSON files, run the migration script:

```bash
./venv/bin/python migrate_platforms.py
```

This will:
- Convert Messenger data to `messenger_groups.json`
- Convert WhatsApp data to `whatsapp_channels.json`
- Group WhatsApp posts by channel name

### 3. Start the Server

```bash
./venv/bin/python app.py
```

The server will start at: **http://localhost:5000**

### 4. Open in Browser

Navigate to `http://localhost:5000` and start exploring!

## Project Structure

```
bot_ui/
├── app.py                      # Flask backend server
├── requirements.txt            # Python dependencies
├── index.html                  # Main HTML page
├── style.css                   # Styles with platform tabs
├── script.js                   # Frontend JavaScript
├── messenger_groups.json       # Messenger data storage
├── whatsapp_channels.json      # WhatsApp data storage
├── migrate_platforms.py        # Data migration script
├── POSTMAN_WHATSAPP_GUIDE.md  # Postman usage guide
├── API_USAGE.md               # Complete API documentation
└── venv/                      # Virtual environment
```

## API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoints

#### 1. Get Available Platforms
```http
GET /api/platforms
```

**Response:**
```json
{
  "platforms": [
    {"name": "messenger", "display_name": "Messenger", "count": 3},
    {"name": "whatsapp", "display_name": "WhatsApp", "count": 5}
  ]
}
```

---

#### 2. Get Groups/Channels List
```http
GET /api/groups?platform={platform}
```

**Parameters:**
- `platform` (required): `messenger` or `whatsapp`

**Example:**
```bash
curl http://localhost:5000/api/groups?platform=messenger
```

**Response (Messenger):**
```json
{
  "groups": [
    {
      "Title": "কাঠ গোলাপ",
      "Sub_Title": "ঢাকা বিভাগের পাত্রী পাত্র",
      "message_count": 20,
      "last_updated": "2025-12-13 01:00:00"
    }
  ]
}
```

**Response (WhatsApp):**
```json
{
  "channels": [
    {
      "Source_name": "Jamuna Television",
      "Source_link": "https://whatsapp.com/channel/...",
      "post_count": 11,
      "Followers": "182,083",
      "Profile_picture": "https://...",
      "last_updated": "2025-12-13 01:00:00"
    }
  ]
}
```

---

#### 3. Get Messages/Posts
```http
GET /api/messages?platform={platform}&title={title}
GET /api/messages?platform={platform}&source={source}
```

**Parameters:**
- `platform` (required): `messenger` or `whatsapp`
- `title` (for Messenger): Group title
- `source` (for WhatsApp): Channel source name

**Example (Messenger):**
```bash
curl "http://localhost:5000/api/messages?platform=messenger&title=কাঠ গোলাপ"
```

**Example (WhatsApp):**
```bash
curl "http://localhost:5000/api/messages?platform=whatsapp&source=Jamuna Television"
```

---

#### 4. Add/Update Data
```http
POST /api/messages?platform={platform}
Content-Type: application/json
```

**Messenger Format:**
```json
{
  "Title": "Group Name",
  "Sub_Title": "Description",
  "messages": [
    {
      "user_name": "John Doe",
      "user_profile_pic": "https://example.com/avatar.jpg",
      "text": "Message text",
      "media": ["https://example.com/image.jpg"],
      "timestamp": "2025-12-13 01:00:00",
      "reactions": {"👍": 5, "❤": 3}
    }
  ]
}
```

**WhatsApp Format:**
```json
{
  "Source_name": "Channel Name",
  "Source_link": "https://whatsapp.com/channel/...",
  "Followers": "1000",
  "Profile_picture": "https://example.com/profile.jpg",
  "posts": [
    {
      "Post_text": "Post text",
      "Post_image": "https://example.com/image.jpg",
      "Post_time": "8:55 PM",
      "Post_reaction": "52",
      "Post_scraping_time": "2025-12-13 01:00:00"
    }
  ]
}
```

**Example (cURL):**
```bash
# Messenger
curl -X POST "http://localhost:5000/api/messages?platform=messenger" \
  -H "Content-Type: application/json" \
  -d '{
    "Title": "New Group",
    "Sub_Title": "Test Group",
    "messages": []
  }'

# WhatsApp
curl -X POST "http://localhost:5000/api/messages?platform=whatsapp" \
  -H "Content-Type: application/json" \
  -d '{
    "Source_name": "Test Channel",
    "posts": [
      {
        "Post_text": "Hello!",
        "Post_time": "1:00 PM"
      }
    ]
  }'
```

**Success Response:**
```json
{
  "success": true,
  "platform": "messenger",
  "title": "New Group",
  "message_count": 0,
  "action": "created"
}
```

## Using with Postman

### Quick Setup:

1. **Create New Request**
   - Method: `POST`
   - URL: `http://localhost:5000/api/messages?platform=whatsapp`

2. **Set Headers**
   - Key: `Content-Type`
   - Value: `application/json`

3. **Set Body** (select `raw` and `JSON`)
   ```json
   {
     "Source_name": "My Channel",
     "posts": [
       {
         "Post_text": "Test from Postman!",
         "Post_time": "Now"
       }
     ]
   }
   ```

4. **Click Send**

See [`POSTMAN_WHATSAPP_GUIDE.md`](POSTMAN_WHATSAPP_GUIDE.md) for detailed instructions.

## Data Format Details

### Required Fields

**Messenger:**
- `Title` (string) - Unique identifier
- `messages` (array) - Array of message objects

**WhatsApp:**
- `Source_name` (string) - Unique identifier
- `posts` (array) - Array of post objects

### Optional Fields

All other fields are optional but recommended for better display:
- Profile pictures
- Timestamps
- Reactions/follower counts
- Media URLs

## Duplicate Prevention

- **Messenger**: Uses `Title` as unique identifier
- **WhatsApp**: Uses `Source_name` as unique identifier

When you POST data with an existing identifier:
- The entire group/channel is **replaced** with new data
- Response will show `"action": "updated"`

When you POST data with a new identifier:
- A new group/channel is **created** at the top of the list
- Response will show `"action": "created"`

## Bengali Language Support

The application fully supports Bengali text:
- UTF-8 encoding throughout
- Noto Sans Bengali font loaded from Google Fonts
- No special configuration needed - just paste Bengali text!

Example:
```json
{
  "Title": "কাঠ গোলাপ",
  "Sub_Title": "ঢাকা বিভাগের পাত্রী পাত্র",
  "messages": [...]
}
```

## Development

### File Watching
The Flask server runs in debug mode with auto-reload:
- Changes to Python files trigger automatic restart
- Frontend changes (HTML/CSS/JS) require browser refresh

### Adding New Platforms
To add support for additional platforms:
1. Add new storage file in `app.py`
2. Update `load_platform_data()` and `save_platform_data()`
3. Add platform tab in `index.html`
4. Add rendering logic in `script.js`

## Troubleshooting

### Server won't start
```bash
# Check if port 5000 is in use
lsof -i :5000

# Kill process if needed
kill -9 <PID>

# Or use a different port
# Edit app.py: app.run(port=5001)
```

### Data not showing
1. Check browser console for errors (F12)
2. Verify JSON format is correct
3. Check server logs for error messages
4. Ensure platform parameter is correct

### Bengali text showing as ???
- Ensure `Content-Type: application/json` header is set
- Check that file encoding is UTF-8
- Verify browser supports Bengali fonts

## Production Deployment

For production use:

1. **Use a production WSGI server:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Add authentication** (recommended)
3. **Use HTTPS** with SSL certificates
4. **Set up database** instead of JSON files for better performance
5. **Add rate limiting** to prevent abuse

## Contributing

Feel free to submit issues or pull requests!

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Support

For questions or issues:
1. Check the [`API_USAGE.md`](API_USAGE.md) for detailed API documentation
2. See [`POSTMAN_WHATSAPP_GUIDE.md`](POSTMAN_WHATSAPP_GUIDE.md) for Postman examples
3. Review the [`walkthrough.md`](.gemini/antigravity/brain/d190d6a8-ab11-4cd9-9295-60ce7418f826/walkthrough.md) for implementation details

---

**Built with ❤️ using Flask, JavaScript, and modern web technologies**
