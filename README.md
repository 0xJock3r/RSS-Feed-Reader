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

