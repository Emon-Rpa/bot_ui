import json
import os

def cleanup_data_structure(data):
    """
    Cleans up 'Unknown' timestamps from the provided data structure.
    Returns (modified_data, was_modified)
    """
    modified = False
    
    if not isinstance(data, (dict, list)):
        return data, False

    # 1. Process Messenger-style nested structures
    # authors -> channels -> messages OR channels -> groups -> messages
    roots = []
    if isinstance(data, dict):
        if 'authors' in data: roots.append((data['authors'], 'channels', 'messages'))
        if 'channels' in data: roots.append((data['channels'], 'groups', 'messages'))
        if 'groups' in data: 
            # Flat Messenger structure
            for group in data['groups']:
                if 'messages' in group:
                    orig = len(group['messages'])
                    group['messages'] = [m for m in group['messages'] if m.get('timestamp') != "Unknown"]
                    if len(group['messages']) < orig: modified = True
    
    for root_list, sub_key, leaf_key in roots:
        for item in root_list:
            if sub_key in item:
                for sub_item in item[sub_key]:
                    if leaf_key in sub_item:
                        orig = len(sub_item[leaf_key])
                        sub_item[leaf_key] = [m for m in sub_item[leaf_key] if m.get('timestamp') != "Unknown"]
                        if len(sub_item[leaf_key]) < orig: modified = True

    # 2. Process WhatsApp-style structures
    # channels (list or dict root) -> posts
    wa_channels = []
    if isinstance(data, dict):
        if 'channels' in data: wa_channels = data['channels']
    elif isinstance(data, list):
        wa_channels = data

    for ch in wa_channels:
        if isinstance(ch, dict) and 'posts' in ch:
            orig = len(ch['posts'])
            ch['posts'] = [p for p in ch['posts'] if p.get('Post_time') != "Unknown" and p.get('Post_scraping_time') != "Unknown"]
            if len(ch['posts']) < orig: modified = True

    return data, modified

def cleanup_file(file_path):
    """Loads a file, cleans it, and saves if modified."""
    if not os.path.exists(file_path):
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return False

    cleaned_data, modified = cleanup_data_structure(data)

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(cleaned_data, f, indent=4, ensure_ascii=False)
        return True
    return False

if __name__ == "__main__":
    # Get the directory where this script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    files = ["messenger_groups.json", "whatsapp_channels.json"]
    for filename in files:
        full_path = os.path.join(base_dir, filename)
        if cleanup_file(full_path):
            print(f"Cleaned {filename}")
        else:
            print(f"No cleanup needed for {filename}")
