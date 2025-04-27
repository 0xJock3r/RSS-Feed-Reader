# 📰 RSS Feed Reader

A simple command-line RSS feed reader to stay updated with your favorite websites and blogs.

## ✨ Features

- 📋 Manage your RSS feed subscriptions
- 🔄 Fetch and display the latest articles
- 📝 Keep track of read and unread items
- 🔍 Read specific feeds or all at once
- 📑 View article summaries
- 🔖 Mark items as read
- 💾 Persistent storage of feeds and read status

## 📋 Requirements

- Python 3.6 or higher
- feedparser library

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/0xJock3r/rss-reader.git
cd rss-reader
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Make the script executable (Unix/Linux/macOS):
```bash
chmod +x main.py
```

## 🔍 Usage

```bash
python main.py <command> [options]
```

## ⚙️ Commands

- `add`: Add a new RSS feed
- `remove`: Remove an RSS feed
- `list`: List all configured feeds
- `read`: Read items from feeds
- `mark-read`: Mark all items in feeds as read
- `clear-history`: Clear read items history

## 📋 Command Options

### Add a feed:
```bash
python main.py add <url> [options]
```

#### Options:

- `-n, --name`: Custom name for the feed

### Remove a feed:
```bash
python main.py remove <name>
```

### List feeds:
```bash
python main.py list
```

### Read feeds:
```bash
python main.py read [feed_name] [options]
```

#### Options:

- `-m, --max`: Maximum number of items to show (default: 10)
- `-a, --all`: Show already read items
- `-r, --mark-read`: Mark items as read

### Mark all as read:
```bash
python main.py mark-read [feed_name]
```

### Clear read history:
```bash
python main.py clear-history
```

### Global options:

- `-c, --config`: Configuration file (default: ~/.rss_reader.json)

## 📝 Examples

### Add a feed:
```bash
python main.py add https://news.ycombinator.com/rss
```

### Add a feed with a custom name:
```bash
python main.py add https://www.reddit.com/r/python/.rss -n "Reddit Python"
```

### List all feeds:
```bash
python main.py list
```

### Read all feeds:
```bash
python main.py read
```

### Read a specific feed:
```bash
python main.py read "Reddit Python"
```

### Read more items:
```bash
python main.py read -m 20
```

### Show all items including read ones:
```bash
python main.py read -a
```

### Mark items as read while reading:
```bash
python main.py read -r
```

### Mark all items in all feeds as read:
```bash
python main.py mark-read
```

### Mark all items in a specific feed as read:
```bash
python main.py mark-read "Reddit Python"
```

### Clear read history:
```bash
python main.py clear-history
```

## 📚 RSS Feed Suggestions

Here are some popular RSS feeds you might want to add:

### News
- BBC News: http://feeds.bbci.co.uk/news/world/rss.xml
- Reuters: http://feeds.reuters.com/reuters/topNews
- NPR: https://feeds.npr.org/1001/rss.xml

### Technology
- Hacker News: https://news.ycombinator.com/rss
- TechCrunch: https://techcrunch.com/feed/
- Wired: https://www.wired.com/feed/rss

### Science
- NASA: https://www.nasa.gov/rss/dyn/breaking_news.rss
- Nature: http://feeds.nature.com/nature/rss/current
- Science Daily: https://www.sciencedaily.com/rss/all.xml

### Programming
- Reddit Python: https://www.reddit.com/r/python/.rss
- Python Insider: https://pythoninsider.blogspot.com/feeds/posts/default
- GitHub Blog: https://github.blog/feed/

## 💡 Tips

- Add a variety of feeds to stay informed about different topics
- Use the `-r` flag when reading to automatically mark items as read
- Use the `-a` flag to see older articles you've already read
- Clear your read history occasionally to keep the database small
- Use this tool in a cron job or scheduled task to check for new articles automatically

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.