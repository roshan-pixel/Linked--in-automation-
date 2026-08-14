# 🚀 LinkedIn 30-Day Post Automation (AI & CDP Powered)

> **Automate 30 consecutive days of scheduled LinkedIn posts — effortlessly, reliably, and hands-free.**

This open-source automation framework allows anyone (even beginners with zero coding experience) to schedule 30 days of high-quality LinkedIn posts at specific times (e.g. 12:00 PM IST daily).

---

## ✨ Features

- 📅 **30-Day Automated Scheduling**: Schedules posts for 30 consecutive future dates with distinct daily content.
- 🎯 **Solves LinkedIn Shadow DOM Issues**: Interacts with LinkedIn's internal shadow root `#interop-outlet` calendar picker deterministically.
- ⏰ **Custom Posting Times**: Set any daily slot (e.g., `12:00 PM`).
- 🤖 **AI & MCP Compatible**: Works seamlessly with local WebBridge / CDP or AI assistant tools (Antigravity, WinClaw, Kimi WebBridge).
- 🔗 **Rich Media Support**: Supports emojis, markdown links, code blocks, and hashtags.

---

## 🚀 Quick Start Guide (For Beginners)

### 1. Prerequisites
Make sure you have installed:
- **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
- **Google Chrome**: Signed in to your LinkedIn account.
- **Kimi WebBridge Daemon**: Running locally on port `10086`.

### 2. Clone the Repository
```bash
git clone https://github.com/roshan-pixel/Linked--in-automation-.git
cd Linked--in-automation-
```

### 3. Run the Automation Script
```bash
python linkedin_automation.py
```

---

## 🛠️ Customizing Your Posts

Open `linkedin_automation.py` and modify the `POSTS` list with your custom daily content and start date:

```python
START_DATE = datetime(2026, 8, 15)  # Set your start date (Year, Month, Day)
POST_TIME_TEXT = "12:00 PM"           # Set your daily post time

POSTS = [
  {"day": 1, "content": "Your post content for Day 1... #hashtags"},
  {"day": 2, "content": "Your post content for Day 2... #hashtags"},
  ...
]
```

---

## 💡 How It Works Under the Hood

1. **Feed Navigation**: Automates navigation to `https://www.linkedin.com/feed/`.
2. **Post Modal Triggering**: Detects the "Start a post" input component.
3. **Shadow DOM Traversal**: Navigates into `#interop-outlet.shadowRoot` to interact with LinkedIn's calendar day buttons (`aria-label="Saturday, August 15, 2026."`).
4. **Time Selection**: Selects `12:00 PM` from the typeahead dropdown list.
5. **Rich Text Formatting**: Populates the editor `.ql-editor` / contenteditable container without breaking line breaks or emojis.
6. **Submission**: Clicks the primary **Schedule** button and verifies the item appears in the queue.

---

## 🛡️ License

Distributed under the **MIT License**. Free to use, modify, and build upon!

Created with ❤️ by [Roshan Singh (@roshan-pixel)](https://github.com/roshan-pixel)
