#!/usr/bin/env python3

import argparse
import json
import os
import sys
import datetime
import textwrap
import feedparser
from datetime import datetime

# Constants
DEFAULT_CONFIG_FILE = os.path.expanduser("~/.rss_reader.json")
DEFAULT_MAX_ITEMS = 10

def load_config(config_file=DEFAULT_CONFIG_FILE):
    """Load configuration from file"""
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: {config_file} is corrupted")
            return {"feeds": [], "read_items": []}
    return {"feeds": [], "read_items": []}

def save_config(config, config_file=DEFAULT_CONFIG_FILE):
    """Save configuration to file"""
    try:
        directory = os.path.dirname(config_file)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving configuration: {e}")
        return False

def add_feed(url, name=None, config_file=DEFAULT_CONFIG_FILE):
    """Add an RSS feed to the configuration"""
    config = load_config(config_file)
    
    # Check if feed already exists
    for feed in config["feeds"]:
        if feed["url"] == url:
            print(f"Feed already exists: {feed['name']}")
            return False
    
    # Try to fetch the feed to validate
    feed_data = feedparser.parse(url)
    if feed_data.get("bozo_exception"):
        print(f"Error parsing feed: {feed_data.get('bozo_exception')}")
        return False
    
    # Use provided name or extract from feed
    if not name:
        name = feed_data.feed.get("title", url)
    
    # Add feed to configuration
    config["feeds"].append({
        "name": name,
        "url": url,
        "added": datetime.now().isoformat()
    })
    
    return save_config(config, config_file)

def remove_feed(name, config_file=DEFAULT_CONFIG_FILE):
    """Remove an RSS feed from the configuration"""
    config = load_config(config_file)
    
    # Find feed by name
    for i, feed in enumerate(config["feeds"]):
        if feed["name"] == name:
            del config["feeds"][i]
            print(f"Feed removed: {name}")
            return save_config(config, config_file)
    
    print(f"Feed not found: {name}")
    return False

def list_feeds(config_file=DEFAULT_CONFIG_FILE):
    """List all RSS feeds"""
    config = load_config(config_file)
    
    if not config["feeds"]:
        print("No feeds configured")
        return
    
    print("\nConfigured Feeds:")
    print("-" * 50)
    for i, feed in enumerate(config["feeds"], 1):
        print(f"{i}. {feed['name']}")
        print(f"   URL: {feed['url']}")
        print(f"   Added: {feed['added']}")
    print("-" * 50)
    print(f"Total: {len(config['feeds'])} feeds")

def read_feed(feed_name=None, max_items=DEFAULT_MAX_ITEMS, show_read=False, 
             mark_read=False, config_file=DEFAULT_CONFIG_FILE):
    """Read items from one or all feeds"""
    config = load_config(config_file)
    
    if not config["feeds"]:
        print("No feeds configured")
        return
    
    feeds_to_read = []
    
    # Determine which feeds to read
    if feed_name:
        for feed in config["feeds"]:
            if feed["name"] == feed_name:
                feeds_to_read.append(feed)
                break
        if not feeds_to_read:
            print(f"Feed not found: {feed_name}")
            return
    else:
        feeds_to_read = config["feeds"]
    
    # Create a set of read item IDs for faster lookup
    read_items = set(config["read_items"])
    newly_read = []
    
    # Read each feed
    for feed_config in feeds_to_read:
        try:
            print(f"\n=== {feed_config['name']} ===\n")
            
            # Fetch feed
            feed = feedparser.parse(feed_config["url"])
            
            if feed.get("bozo_exception"):
                print(f"Error parsing feed: {feed.get('bozo_exception')}")
                continue
            
            # Get items
            items = feed.get("items", [])
            if not items:
                print("No items found in feed")
                continue
            
            # Sort by published date if available
            for item in items:
                if "published_parsed" in item:
                    item["_sort_date"] = item["published_parsed"]
                elif "updated_parsed" in item:
                    item["_sort_date"] = item["updated_parsed"]
                else:
                    item["_sort_date"] = None
            
            items.sort(key=lambda x: x["_sort_date"] if x["_sort_date"] else (0,), reverse=True)
            
            # Display items
            item_count = 0
            for i, item in enumerate(items):
                # Construct a unique ID for the item
                item_id = f"{feed_config['url']}:{item.get('id', item.get('link', ''))}"
                
                # Skip if already read and not showing read items
                if item_id in read_items and not show_read:
                    continue
                
                # Limit the number of items shown
                item_count += 1
                if item_count > max_items:
                    break
                
                # Display item
                title = item.get("title", "No title")
                link = item.get("link", "No link")
                date = ""
                
                if "published" in item:
                    date = item["published"]
                elif "updated" in item:
                    date = item["updated"]
                
                # Determine read status
                status = "[Read]" if item_id in read_items else "[New]"
                
                print(f"{i+1}. {status} {title}")
                print(f"   Date: {date}")
                print(f"   Link: {link}")
                
                # Get summary/content
                summary = ""
                if "summary" in item:
                    summary = item["summary"]
                elif "description" in item:
                    summary = item["description"]
                elif "content" in item:
                    for content in item["content"]:
                        if "value" in content:
                            summary = content["value"]
                            break
                
                # Strip HTML and display
                from html.parser import HTMLParser
                
                class MLStripper(HTMLParser):
                    def __init__(self):
                        super().__init__()
                        self.reset()
                        self.strict = False
                        self.convert_charrefs = True
                        self.text = []
                    
                    def handle_data(self, d):
                        self.text.append(d)
                    
                    def get_data(self):
                        return ''.join(self.text)
                
                def strip_tags(html):
                    s = MLStripper()
                    s.feed(html)
                    return s.get_data()
                
                if summary:
                    # Strip HTML tags
                    summary = strip_tags(summary)
                    
                    # Wrap text
                    summary = textwrap.fill(summary, width=70)
                    
                    # Limit length
                    if len(summary) > 300:
                        summary = summary[:297] + "..."
                    
                    print(f"   Summary: {summary}")
                
                print("")
                
                # Mark as read if requested
                if mark_read and item_id not in read_items:
                    read_items.add(item_id)
                    newly_read.append(item_id)
        
        except Exception as e:
            print(f"Error reading feed {feed_config['name']}: {e}")
    
    # Update configuration with newly read items
    if newly_read:
        config["read_items"].extend(newly_read)
        save_config(config, config_file)

def mark_all_read(feed_name=None, config_file=DEFAULT_CONFIG_FILE):
    """Mark all items in a feed as read"""
    config = load_config(config_file)
    
    if not config["feeds"]:
        print("No feeds configured")
        return
    
    feeds_to_mark = []
    
    # Determine which feeds to mark
    if feed_name:
        for feed in config["feeds"]:
            if feed["name"] == feed_name:
                feeds_to_mark.append(feed)
                break
        if not feeds_to_mark:
            print(f"Feed not found: {feed_name}")
            return
    else:
        feeds_to_mark = config["feeds"]
    
    # Create a set of read item IDs for faster lookup
    read_items = set(config["read_items"])
    newly_read = []
    
    # Mark each feed
    for feed_config in feeds_to_mark:
        try:
            # Fetch feed
            feed = feedparser.parse(feed_config["url"])
            
            if feed.get("bozo_exception"):
                print(f"Error parsing feed: {feed.get('bozo_exception')}")
                continue
            
            # Get items
            items = feed.get("items", [])
            if not items:
                continue
            
            # Mark each item as read
            for item in items:
                item_id = f"{feed_config['url']}:{item.get('id', item.get('link', ''))}"
                if item_id not in read_items:
                    newly_read.append(item_id)
        
        except Exception as e:
            print(f"Error marking feed {feed_config['name']}: {e}")
    
    # Update configuration with newly read items
    if newly_read:
        config["read_items"].extend(newly_read)
        save_config(config, config_file)
        print(f"Marked {len(newly_read)} items as read")
    else:
        print("No new items to mark as read")

def clear_read_history(config_file=DEFAULT_CONFIG_FILE):
    """Clear the read history"""
    config = load_config(config_file)
    
    if not config["read_items"]:
        print("Read history is already empty")
        return
    
    count = len(config["read_items"])
    config["read_items"] = []
    
    if save_config(config, config_file):
        print(f"Cleared {count} items from read history")

def main():
    parser = argparse.ArgumentParser(description="Simple RSS Feed Reader")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Add feed command
    add_parser = subparsers.add_parser("add", help="Add a new RSS feed")
    add_parser.add_argument("url", help="URL of the RSS feed")
    add_parser.add_argument("-n", "--name", help="Name for the feed")
    
    # Remove feed command
    remove_parser = subparsers.add_parser("remove", help="Remove an RSS feed")
    remove_parser.add_argument("name", help="Name of the feed to remove")
    
    # List feeds command
    list_parser = subparsers.add_parser("list", help="List all configured feeds")
    
    # Read feed command
    read_parser = subparsers.add_parser("read", help="Read items from feeds")
    read_parser.add_argument("feed", nargs="?", help="Name of the feed to read (default: all feeds)")
    read_parser.add_argument("-m", "--max", type=int, default=DEFAULT_MAX_ITEMS, 
                          help=f"Maximum number of items to show (default: {DEFAULT_MAX_ITEMS})")
    read_parser.add_argument("-a", "--all", action="store_true", help="Show already read items")
    read_parser.add_argument("-r", "--mark-read", action="store_true", help="Mark items as read")
    
    # Mark all read command
    mark_parser = subparsers.add_parser("mark-read", help="Mark all items in feeds as read")
    mark_parser.add_argument("feed", nargs="?", help="Name of the feed to mark (default: all feeds)")
    
    # Clear read history command
    clear_parser = subparsers.add_parser("clear-history", help="Clear read items history")
    
    # Global options
    parser.add_argument("-c", "--config", default=DEFAULT_CONFIG_FILE, 
                       help=f"Configuration file (default: {DEFAULT_CONFIG_FILE})")
    
    args = parser.parse_args()
    
    if args.command == "add":
        if add_feed(args.url, args.name, args.config):
            print(f"Feed added successfully")
    
    elif args.command == "remove":
        remove_feed(args.name, args.config)
    
    elif args.command == "list":
        list_feeds(args.config)
    
    elif args.command == "read":
        read_feed(args.feed, args.max, args.all, args.mark_read, args.config)
    
    elif args.command == "mark-read":
        mark_all_read(args.feed, args.config)
    
    elif args.command == "clear-history":
        clear_read_history(args.config)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
