#!/usr/bin/env python3
"""
Migration script to convert old single-group JSON to new multi-group format
"""

import json
import os
from datetime import datetime

OLD_FILE = 'কাঠ গোলাপ.json'
NEW_FILE = 'all_groups.json'

def migrate_data():
    """Migrate old format to new format"""
    
    # Check if old file exists
    if not os.path.exists(OLD_FILE):
        print(f"❌ Old file '{OLD_FILE}' not found. Nothing to migrate.")
        return
    
    # Check if new file already exists
    if os.path.exists(NEW_FILE):
        print(f"⚠️  New file '{NEW_FILE}' already exists.")
        response = input("Do you want to add the old data to it? (y/n): ")
        if response.lower() != 'y':
            print("Migration cancelled.")
            return
    
    # Load old data
    try:
        with open(OLD_FILE, 'r', encoding='utf-8') as f:
            old_data = json.load(f)
        print(f"✅ Loaded old data from '{OLD_FILE}'")
        print(f"   Title: {old_data.get('Title')}")
        print(f"   Messages: {len(old_data.get('messages', []))}")
    except Exception as e:
        print(f"❌ Error loading old file: {e}")
        return
    
    # Load existing new data or create empty structure
    if os.path.exists(NEW_FILE):
        try:
            with open(NEW_FILE, 'r', encoding='utf-8') as f:
                new_data = json.load(f)
        except:
            new_data = {"groups": []}
    else:
        new_data = {"groups": []}
    
    # Add timestamp to old data
    old_data['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Check if this group already exists
    group_exists = False
    for i, group in enumerate(new_data['groups']):
        if group.get('Title') == old_data.get('Title'):
            print(f"⚠️  Group '{old_data.get('Title')}' already exists. Updating it.")
            new_data['groups'][i] = old_data
            group_exists = True
            break
    
    # If not exists, add to beginning
    if not group_exists:
        new_data['groups'].insert(0, old_data)
        print(f"✅ Added new group '{old_data.get('Title')}'")
    
    # Save new data
    try:
        with open(NEW_FILE, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)
        print(f"✅ Successfully saved to '{NEW_FILE}'")
        print(f"   Total groups: {len(new_data['groups'])}")
    except Exception as e:
        print(f"❌ Error saving new file: {e}")
        return
    
    print("\n✅ Migration completed successfully!")
    print(f"\nYou can now refresh your browser to see the data.")

if __name__ == '__main__':
    print("=== Data Migration Script ===\n")
    migrate_data()
