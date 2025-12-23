#!/usr/bin/env python3
"""
Clean up messenger_groups.json by removing the old 'groups' key
"""

import json

MESSENGER_FILE = 'messenger_groups.json'

def cleanup_data():
    """Remove old groups structure"""
    
    with open(MESSENGER_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Remove old groups key if it exists
    if 'groups' in data:
        print(f"Removing old 'groups' key with {len(data['groups'])} items")
        del data['groups']
    
    # Save cleaned data
    with open(MESSENGER_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"\n✅ Cleanup complete!")
    print(f"   - Channels: {len(data.get('channels', []))}")
    print(f"   - Total groups: {sum(len(ch.get('groups', [])) for ch in data.get('channels', []))}")

if __name__ == '__main__':
    cleanup_data()
