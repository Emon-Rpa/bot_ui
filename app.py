from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__, static_folder='.')
CORS(app)

# Path to the all groups JSON file
ALL_GROUPS_FILE = 'all_groups.json'

def load_all_groups():
    """Load all message groups from file"""
    try:
        if os.path.exists(ALL_GROUPS_FILE):
            with open(ALL_GROUPS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {"groups": []}
    except Exception as e:
        print(f"Error loading groups: {e}")
        return {"groups": []}

def save_all_groups(data):
    """Save all message groups to file"""
    try:
        with open(ALL_GROUPS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Error saving groups: {e}")
        return False

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/api/groups', methods=['GET'])
def get_all_groups():
    """Get list of all groups (titles only)"""
    try:
        all_data = load_all_groups()
        groups_list = [
            {
                "Title": group.get("Title", "Untitled"),
                "Sub_Title": group.get("Sub_Title", ""),
                "message_count": len(group.get("messages", [])),
                "last_updated": group.get("last_updated", "")
            }
            for group in all_data.get("groups", [])
        ]
        return jsonify({"groups": groups_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/messages', methods=['GET', 'POST'])
def handle_messages():
    """API endpoint to get or update messages"""
    
    if request.method == 'GET':
        # GET: Return all groups or specific group
        try:
            title = request.args.get('title')
            all_data = load_all_groups()
            
            if title:
                # Return specific group by title
                for group in all_data.get("groups", []):
                    if group.get("Title") == title:
                        return jsonify(group)
                return jsonify({'error': 'Group not found'}), 404
            else:
                # Return all groups
                return jsonify(all_data)
                
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'POST':
        # POST: Add or update a group (merge by Title)
        try:
            # Get JSON data from request
            new_group = request.get_json()
            
            # Validate required fields
            if not new_group:
                return jsonify({'error': 'No JSON data provided'}), 400
            
            if 'Title' not in new_group or 'messages' not in new_group:
                return jsonify({'error': 'Invalid format. Required fields: Title, messages'}), 400
            
            # Load existing groups
            all_data = load_all_groups()
            groups = all_data.get("groups", [])
            
            # Add timestamp
            new_group['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Check if group with same Title exists
            group_exists = False
            for i, group in enumerate(groups):
                if group.get("Title") == new_group.get("Title"):
                    # Update existing group (replace it)
                    groups[i] = new_group
                    group_exists = True
                    break
            
            # If group doesn't exist, add it to the beginning
            if not group_exists:
                groups.insert(0, new_group)
            
            # Save updated data
            all_data["groups"] = groups
            if save_all_groups(all_data):
                return jsonify({
                    'success': True,
                    'message': 'Group saved successfully',
                    'title': new_group.get('Title'),
                    'message_count': len(new_group.get('messages', [])),
                    'total_groups': len(groups),
                    'action': 'updated' if group_exists else 'created'
                }), 200
            else:
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
    print(f"Starting server...")
    print(f"Open your browser at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
