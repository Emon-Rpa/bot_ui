#!/usr/bin/env python3
"""
Migration script to convert data to multi-platform format
- Messenger: groups from all_groups.json or কাঠ গোলাপ.json
- WhatsApp: channels from Jamuna_Television.json, Netflix.json, etc.
"""

import json
import os
import glob
from datetime import datetime

# File paths
MESSENGER_OUTPUT = 'messenger_groups.json'
WHATSAPP_OUTPUT = 'whatsapp_channels.json'

def migrate_messenger_data():
    """Migrate Messenger data from existing files"""
    messenger_data = {"groups": []}
    
    # Try to load from all_groups.json first
    if os.path.exists('all_groups.json'):
        try:
            with open('all_groups.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                messenger_data = data
                print(f"✅ Loaded Messenger data from 'all_groups.json'")
                print(f"   Groups: {len(messenger_data.get('groups', []))}")
        except Exception as e:
            print(f"⚠️  Error loading all_groups.json: {e}")
    
    # Also check for old single-group format
    old_file = 'কাঠ গোলাপ.json'
    if os.path.exists(old_file):
        try:
            with open(old_file, 'r', encoding='utf-8') as f:
                old_data = json.load(f)
            
            # Check if this group already exists
            title = old_data.get('Title')
            exists = any(g.get('Title') == title for g in messenger_data.get('groups', []))
            
            if not exists and title:
                old_data['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                messenger_data['groups'].insert(0, old_data)
                print(f"✅ Added group '{title}' from old format")
        except Exception as e:
            print(f"⚠️  Error loading {old_file}: {e}")
    
    # Save Messenger data
    if messenger_data.get('groups'):
        try:
            with open(MESSENGER_OUTPUT, 'w', encoding='utf-8') as f:
                json.dump(messenger_data, f, ensure_ascii=False, indent=4)
            print(f"✅ Saved Messenger data to '{MESSENGER_OUTPUT}'")
            print(f"   Total groups: {len(messenger_data['groups'])}")
            return True
        except Exception as e:
            print(f"❌ Error saving Messenger data: {e}")
            return False
    else:
        print("ℹ️  No Messenger data to migrate")
        return True

def migrate_whatsapp_data():
    """Migrate WhatsApp data from JSON files"""
    whatsapp_data = {"channels": []}
    
    # Find all WhatsApp JSON files (arrays of posts)
    json_files = glob.glob('*.json')
    whatsapp_files = []
    
    for file in json_files:
        # Skip our output files and known Messenger files
        if file in [MESSENGER_OUTPUT, WHATSAPP_OUTPUT, 'all_groups.json', 'কাঠ গোলাপ.json']:
            continue
        
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check if it's a WhatsApp format (array of posts with Source_name)
            if isinstance(data, list) and len(data) > 0 and 'Source_name' in data[0]:
                whatsapp_files.append(file)
        except:
            continue
    
    print(f"\nFound {len(whatsapp_files)} WhatsApp files: {whatsapp_files}")
    
    # Process each WhatsApp file
    for file in whatsapp_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                posts = json.load(f)
            
            if not posts:
                continue
            
            # Group posts by Source_name
            channels_dict = {}
            for post in posts:
                source_name = post.get('Source_name', 'Unknown')
                if source_name not in channels_dict:
                    channels_dict[source_name] = {
                        'Source_name': source_name,
                        'Source_link': post.get('Source_link', ''),
                        'Followers': post.get('Followers', '0'),
                        'Profile_picture': post.get('Profile_picture', ''),
                        'posts': [],
                        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                
                # Add post to channel
                channels_dict[source_name]['posts'].append({
                    'Post_text': post.get('Post_text'),
                    'Post_image': post.get('Post_image'),
                    'Post_time': post.get('Post_time'),
                    'Post_reaction': post.get('Post_reaction'),
                    'Post_scraping_time': post.get('Post_scraping_time')
                })
            
            # Add channels to main data
            for channel in channels_dict.values():
                # Check if channel already exists
                exists = any(c.get('Source_name') == channel['Source_name'] 
                           for c in whatsapp_data['channels'])
                
                if not exists:
                    whatsapp_data['channels'].append(channel)
                    print(f"✅ Added channel '{channel['Source_name']}' with {len(channel['posts'])} posts")
        
        except Exception as e:
            print(f"⚠️  Error processing {file}: {e}")
    
    # Save WhatsApp data
    if whatsapp_data.get('channels'):
        try:
            with open(WHATSAPP_OUTPUT, 'w', encoding='utf-8') as f:
                json.dump(whatsapp_data, f, ensure_ascii=False, indent=4)
            print(f"\n✅ Saved WhatsApp data to '{WHATSAPP_OUTPUT}'")
            print(f"   Total channels: {len(whatsapp_data['channels'])}")
            for channel in whatsapp_data['channels']:
                print(f"   - {channel['Source_name']}: {len(channel['posts'])} posts")
            return True
        except Exception as e:
            print(f"❌ Error saving WhatsApp data: {e}")
            return False
    else:
        print("ℹ️  No WhatsApp data to migrate")
        return True

def main():
    print("=== Multi-Platform Data Migration ===\n")
    
    print("📱 Migrating Messenger data...")
    messenger_success = migrate_messenger_data()
    
    print("\n💬 Migrating WhatsApp data...")
    whatsapp_success = migrate_whatsapp_data()
    
    if messenger_success and whatsapp_success:
        print("\n✅ Migration completed successfully!")
        print("\nYou can now:")
        print("1. Restart the Flask server")
        print("2. Refresh your browser")
        print("3. Switch between Messenger and WhatsApp platforms")
    else:
        print("\n⚠️  Migration completed with some errors")

if __name__ == '__main__':
    main()
