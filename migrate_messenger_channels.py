#!/usr/bin/env python3
"""
Migration script to convert messenger_groups.json from flat structure to nested channel/group structure.

Old structure:
{
  "groups": [
    {"Title": "...", "messages": [...]}
  ]
}

New structure:
{
  "channels": [
    {
      "author_id": "...",
      "author_url": "...",
      "channel_name": "...",
      "icon": "...",
      "groups": [
        {"source": "...", "Title": "...", "messages": [...]}
      ]
    }
  ]
}
"""

import json
import os
from datetime import datetime

MESSENGER_FILE = 'messenger_groups.json'
BACKUP_FILE = f'messenger_groups_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'

def migrate_messenger_data():
    """Migrate messenger data from flat to nested structure"""
    
    # Check if file exists
    if not os.path.exists(MESSENGER_FILE):
        print(f"Error: {MESSENGER_FILE} not found")
        return False
    
    # Load existing data
    print(f"Loading {MESSENGER_FILE}...")
    with open(MESSENGER_FILE, 'r', encoding='utf-8') as f:
        old_data = json.load(f)
    
    # Create backup
    print(f"Creating backup: {BACKUP_FILE}...")
    with open(BACKUP_FILE, 'w', encoding='utf-8') as f:
        json.dump(old_data, f, ensure_ascii=False, indent=4)
    
    # Check if already in new format
    if 'channels' in old_data:
        print("Data is already in the new format!")
        return True
    
    # Convert to new structure
    print("Converting to new structure...")
    channels_map = {}  # author_id -> channel data
    
    for group in old_data.get('groups', []):
        author_id = group.get('author_id')
        
        if not author_id:
            print(f"Warning: Group '{group.get('Title', 'Unknown')}' has no author_id, skipping...")
            continue
        
        # Create channel if it doesn't exist
        if author_id not in channels_map:
            channels_map[author_id] = {
                'author_id': author_id,
                'author_url': group.get('author_url', ''),
                'channel_name': group.get('Title', 'Unknown Channel'),
                'icon': group.get('icon', ''),
                'groups': []
            }
        
        # Add group to channel
        group_data = {
            'source': group.get('source', ''),
            'Title': group.get('Title', ''),
            'Sub_Title': group.get('Sub_Title', ''),
            'messages': group.get('messages', []),
            'last_updated': group.get('last_updated', '')
        }
        
        channels_map[author_id]['groups'].append(group_data)
    
    # Convert to list
    new_data = {
        'channels': list(channels_map.values())
    }
    
    # Save new structure
    print(f"Saving new structure to {MESSENGER_FILE}...")
    with open(MESSENGER_FILE, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)
    
    print(f"\n✅ Migration complete!")
    print(f"   - Channels created: {len(new_data['channels'])}")
    print(f"   - Total groups: {sum(len(ch['groups']) for ch in new_data['channels'])}")
    print(f"   - Backup saved: {BACKUP_FILE}")
    
    return True

if __name__ == '__main__':
    migrate_messenger_data()
