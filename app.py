from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import json
import os
from datetime import datetime
from cleanup_unknown_timestamps import cleanup_data_structure

app = Flask(__name__, static_folder='.')
CORS(app)

# Platform storage files
MESSENGER_FILE = 'messenger_groups.json'
WHATSAPP_FILE = 'whatsapp_channels.json'

def load_platform_data(platform):
    """Load data for a specific platform"""
    file_map = {
        'messenger': MESSENGER_FILE,
        'whatsapp': WHATSAPP_FILE
    }
    
    file_path = file_map.get(platform.lower())
    if not file_path:
        return None
    
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"Loaded {platform} data: {data is not None}")
                if data:
                    print(f"Keys in {platform} data: {list(data.keys())}")
                    if 'authors' in data:
                        print(f"Number of authors: {len(data['authors'])}")
                    if 'channels' in data:
                        print(f"Number of channels: {len(data['channels'])}")
                    
                    # Automate cleanup of 'Unknown' timestamps
                    data, was_modified = cleanup_data_structure(data)
                    if was_modified:
                        print(f"Automated cleanup: Removed unknown timestamps from {platform} data")
                        # Explicitly save the cleaned data back to ensure it's effective for future loads
                        save_platform_data(platform, data)
                return data
        else:
            # Return empty structure based on platform
            if platform.lower() == 'messenger':
                return {"authors": []}
            else:
                return {"channels": []}
    except Exception as e:
        print(f"Error loading {platform} data: {e}")
        return None

def save_platform_data(platform, data):
    """Save data for a specific platform"""
    file_map = {
        'messenger': MESSENGER_FILE,
        'whatsapp': WHATSAPP_FILE
    }
    
    file_path = file_map.get(platform.lower())
    if not file_path:
        return False
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Error saving {platform} data: {e}")
        return False

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/api/platforms', methods=['GET'])
def get_platforms():
    """Get list of available platforms"""
    platforms = []
    
    # Check Messenger
    messenger_data = load_platform_data('messenger')
    if messenger_data:
        platforms.append({
            'name': 'messenger',
            'display_name': 'Messenger',
            'count': len(messenger_data.get('authors', []))
        })
    
    # Check WhatsApp
    whatsapp_data = load_platform_data('whatsapp')
    if whatsapp_data:
        channels = whatsapp_data.get('channels', [])
        print(f"WhatsApp channels found: {len(channels)}")
        platforms.append({
            'name': 'whatsapp',
            'display_name': 'WhatsApp',
            'count': len(channels)
        })
    
    print(f"Returning platforms: {[p['name'] for p in platforms]}")
    return jsonify({'platforms': platforms})

@app.route('/api/groups', methods=['GET'])
def get_groups():
    """Get list of groups/channels for a platform"""
    platform = request.args.get('platform', 'messenger').lower()
    
    try:
        data = load_platform_data(platform)
        if not data:
            return jsonify({'error': 'Invalid platform'}), 400
        
        if platform == 'messenger':
            # New nested structure: authors with channels
            authors_list = []
            for author in data.get("authors", []):
                author_info = {
                    "author_id": author.get("author_id", ""),
                    "author_url": author.get("author_url", ""),
                    "author_name": author.get("author_name", "Unknown Author"),
                    "channels": []
                }
                
                # Add channels under this author
                for channel in author.get("channels", []):
                    channel_info = {
                        "source": channel.get("source", ""),
                        "Title": channel.get("Title", "Untitled"),
                        "Sub_Title": channel.get("Sub_Title", ""),
                        "icon": channel.get("icon", ""),
                        "message_count": len(channel.get("messages", [])),
                        "last_updated": channel.get("last_updated", "")
                    }
                    author_info["channels"].append(channel_info)
                
                authors_list.append(author_info)
            
            return jsonify({"authors": authors_list})
        
        elif platform == 'whatsapp':
            channels_list = [
                {
                    "Source_name": channel.get("Source_name", "Untitled"),
                    "Source_link": channel.get("Source_link", ""),
                    "post_count": len(channel.get("posts", [])),
                    "Followers": channel.get("Followers", "0"),
                    "Profile_picture": channel.get("Profile_picture", ""),
                    "last_updated": channel.get("last_updated", "")
                }
                for channel in data.get("channels", [])
            ]
            print(f"Returning {len(channels_list)} WhatsApp channels")
            return jsonify({"channels": channels_list})
        
        print(f"Unknown platform or no data for: {platform}")
        return jsonify({'error': 'No data found for platform'}), 404
        
    except Exception as e:
        print(f"Error in get_groups: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/messages', methods=['GET', 'POST'])
def handle_messages():
    """API endpoint to get or update messages"""
    platform = request.args.get('platform', 'messenger').lower()
    
    if request.method == 'GET':
        # GET: Return specific group/channel
        try:
            data = load_platform_data(platform)
            
            if not data:
                return jsonify({'error': 'Invalid platform'}), 400
            
            if platform == 'messenger':
                # New structure: use author_id and source to find channel
                author_id = request.args.get('author_id')
                source = request.args.get('source')
                
                if not author_id or not source:
                    return jsonify({'error': 'author_id and source parameters required'}), 400
                
                # Find author by author_id
                for author in data.get("authors", []):
                    if author.get("author_id") == author_id:
                        # Find channel by source within this author
                        for channel in author.get("channels", []):
                            if channel.get("source") == source:
                                # Add author info to response
                                response = channel.copy()
                                response['author_name'] = author.get('author_name', '')
                                response['author_id'] = author_id
                                response['author_url'] = author.get('author_url', '')
                                return jsonify(response)
                        
                        return jsonify({'error': 'Channel not found in author'}), 404
                
                return jsonify({'error': 'Author not found'}), 404
            
            elif platform == 'whatsapp':
                # Return specific channel by source name
                identifier = request.args.get('source')
                for channel in data.get("channels", []):
                    if channel.get("Source_name") == identifier:
                        return jsonify(channel)
                return jsonify({'error': 'Channel not found'}), 404
                
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'POST':
        # POST: Append new messages to existing group/channel with duplicate detection
        try:
            new_item = request.get_json()
            
            if not new_item:
                return jsonify({'error': 'No JSON data provided'}), 400
            
            data = load_platform_data(platform)
            if not data:
                return jsonify({'error': 'Invalid platform'}), 400
            
            # Ensure new input data is also cleaned before processing
            new_item, _ = cleanup_data_structure(new_item)
            
            new_item['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            if platform == 'messenger':
                # Messenger: use author_id and source as unique identifiers
                if 'author_id' not in new_item or 'source' not in new_item or 'messages' not in new_item:
                    return jsonify({'error': 'Invalid format. Required: author_id, source, messages'}), 400
                
                authors = data.get("authors", [])
                author_exists = False
                channel_exists = False
                new_messages = new_item.get('messages', [])
                total_new = len(new_messages)
                added_count = 0
                duplicate_count = 0
                
                author_id = new_item.get('author_id')
                source = new_item.get('source')
                
                # Find or create author
                for i, author in enumerate(authors):
                    if author.get("author_id") == author_id:
                        author_exists = True
                        channels = author.get('channels', [])
                        
                        # Find or create channel within author
                        for j, channel in enumerate(channels):
                            if channel.get("source") == source:
                                channel_exists = True
                                existing_messages = channel.get('messages', [])
                                
                                # Check for duplicates and append only new messages
                                for new_msg in new_messages:
                                    is_duplicate = False
                                    for existing_msg in existing_messages:
                                        if (existing_msg.get('user_name') == new_msg.get('user_name') and
                                            existing_msg.get('text') == new_msg.get('text') and
                                            existing_msg.get('timestamp') == new_msg.get('timestamp')):
                                            is_duplicate = True
                                            duplicate_count += 1
                                            break
                                    
                                    if not is_duplicate:
                                        existing_messages.append(new_msg)
                                        added_count += 1
                                
                                channels[j]['messages'] = existing_messages
                                channels[j]['last_updated'] = new_item['last_updated']
                                channels[j]['Title'] = new_item.get('Title', channel.get('Title', ''))
                                channels[j]['Sub_Title'] = new_item.get('Sub_Title', channel.get('Sub_Title', ''))
                                if new_item.get('icon'):
                                    channels[j]['icon'] = new_item['icon']
                                break
                        
                        if not channel_exists:
                            # New channel in existing author
                            new_channel = {
                                'source': source,
                                'Title': new_item.get('Title', ''),
                                'Sub_Title': new_item.get('Sub_Title', ''),
                                'icon': new_item.get('icon', ''),
                                'messages': new_messages,
                                'last_updated': new_item['last_updated']
                            }
                            channels.insert(0, new_channel)
                            added_count = total_new
                        
                        authors[i]['channels'] = channels
                        # Update author metadata
                        authors[i]['author_name'] = new_item.get('Title', author.get('author_name', ''))
                        authors[i]['author_url'] = new_item.get('author_url', author.get('author_url', ''))
                        break
                
                if not author_exists:
                    # New author with new channel
                    new_author = {
                        'author_id': author_id,
                        'author_url': new_item.get('author_url', ''),
                        'author_name': new_item.get('Title', 'Unknown Author'),
                        'channels': [
                            {
                                'source': source,
                                'Title': new_item.get('Title', ''),
                                'Sub_Title': new_item.get('Sub_Title', ''),
                                'icon': new_item.get('icon', ''),
                                'messages': new_messages,
                                'last_updated': new_item['last_updated']
                            }
                        ]
                    }
                    authors.insert(0, new_author)
                    added_count = total_new
                
                data["authors"] = authors
                
                if save_platform_data(platform, data):
                    return jsonify({
                        'success': True,
                        'platform': 'messenger',
                        'author_id': author_id,
                        'source': source,
                        'title': new_item.get('Title'),
                        'total_messages_sent': total_new,
                        'messages_added': added_count,
                        'duplicates_skipped': duplicate_count,
                        'author_action': 'updated' if author_exists else 'created',
                        'channel_action': 'updated' if channel_exists else 'created'
                    }), 200
            
            elif platform == 'whatsapp':
                # WhatsApp: use Source_name as unique identifier
                if 'Source_name' not in new_item or 'posts' not in new_item:
                    return jsonify({'error': 'Invalid format. Required: Source_name, posts'}), 400
                
                channels = data.get("channels", [])
                channel_exists = False
                new_posts = new_item.get('posts', [])
                total_new = len(new_posts)
                added_count = 0
                duplicate_count = 0
                
                for i, channel in enumerate(channels):
                    if channel.get("Source_name") == new_item.get("Source_name"):
                        channel_exists = True
                        existing_posts = channel.get('posts', [])
                        
                        # Check for duplicates and append only new posts
                        for new_post in new_posts:
                            is_duplicate = False
                            for existing_post in existing_posts:
                                if (existing_post.get('Post_text') == new_post.get('Post_text') and
                                    existing_post.get('Post_time') == new_post.get('Post_time') and
                                    existing_post.get('Post_image') == new_post.get('Post_image')):
                                    is_duplicate = True
                                    duplicate_count += 1
                                    break
                            
                            if not is_duplicate:
                                existing_posts.append(new_post)
                                added_count += 1
                        
                        channels[i]['posts'] = existing_posts
                        channels[i]['last_updated'] = new_item['last_updated']
                        # Update other fields if provided
                        for field in ['Source_link', 'Followers', 'Profile_picture']:
                            if field in new_item:
                                channels[i][field] = new_item[field]
                        break
                
                if not channel_exists:
                    # New channel, add all posts
                    channels.insert(0, new_item)
                    added_count = total_new
                
                data["channels"] = channels
                
                if save_platform_data(platform, data):
                    return jsonify({
                        'success': True,
                        'platform': 'whatsapp',
                        'source_name': new_item.get('Source_name'),
                        'total_posts_sent': total_new,
                        'posts_added': added_count,
                        'duplicates_skipped': duplicate_count,
                        'action': 'updated' if channel_exists else 'created'
                    }), 200
            
            return jsonify({'error': 'Failed to save data'}), 500
            
        except json.JSONDecodeError:
            return jsonify({'error': 'Invalid JSON format'}), 400
        except Exception as e:
            return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('.', path)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Multi-Platform Message Viewer...")
    print(f"Server will run on port {port}")
    app.run(debug=False, host='0.0.0.0', port=port)
