from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import json
import os
from datetime import datetime

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
                return json.load(f)
        else:
            # Return empty structure based on platform
            if platform.lower() == 'messenger':
                return {"groups": []}
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
            'count': len(messenger_data.get('groups', []))
        })
    
    # Check WhatsApp
    whatsapp_data = load_platform_data('whatsapp')
    if whatsapp_data:
        platforms.append({
            'name': 'whatsapp',
            'display_name': 'WhatsApp',
            'count': len(whatsapp_data.get('channels', []))
        })
    
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
            groups_list = [
                {
                    "Title": group.get("Title", "Untitled"),
                    "Sub_Title": group.get("Sub_Title", ""),
                    "message_count": len(group.get("messages", [])),
                    "last_updated": group.get("last_updated", "")
                }
                for group in data.get("groups", [])
            ]
            return jsonify({"groups": groups_list})
        
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
            return jsonify({"channels": channels_list})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/messages', methods=['GET', 'POST'])
def handle_messages():
    """API endpoint to get or update messages"""
    platform = request.args.get('platform', 'messenger').lower()
    
    if request.method == 'GET':
        # GET: Return specific group/channel
        try:
            identifier = request.args.get('title') or request.args.get('source')
            data = load_platform_data(platform)
            
            if not data:
                return jsonify({'error': 'Invalid platform'}), 400
            
            if platform == 'messenger':
                # Return specific group by title
                for group in data.get("groups", []):
                    if group.get("Title") == identifier:
                        return jsonify(group)
                return jsonify({'error': 'Group not found'}), 404
            
            elif platform == 'whatsapp':
                # Return specific channel by source name
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
            
            new_item['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            if platform == 'messenger':
                # Messenger: use Title as unique identifier
                if 'Title' not in new_item or 'messages' not in new_item:
                    return jsonify({'error': 'Invalid format. Required: Title, messages'}), 400
                
                groups = data.get("groups", [])
                group_exists = False
                new_messages = new_item.get('messages', [])
                total_new = len(new_messages)
                added_count = 0
                duplicate_count = 0
                
                for i, group in enumerate(groups):
                    if group.get("Title") == new_item.get("Title"):
                        group_exists = True
                        existing_messages = group.get('messages', [])
                        
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
                        
                        groups[i]['messages'] = existing_messages
                        groups[i]['last_updated'] = new_item['last_updated']
                        groups[i]['Sub_Title'] = new_item.get('Sub_Title', group.get('Sub_Title', ''))
                        break
                
                if not group_exists:
                    # New group, add all messages
                    groups.insert(0, new_item)
                    added_count = total_new
                
                data["groups"] = groups
                
                if save_platform_data(platform, data):
                    return jsonify({
                        'success': True,
                        'platform': 'messenger',
                        'title': new_item.get('Title'),
                        'total_messages_sent': total_new,
                        'messages_added': added_count,
                        'duplicates_skipped': duplicate_count,
                        'action': 'updated' if group_exists else 'created'
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
