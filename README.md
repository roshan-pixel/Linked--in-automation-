# 🤖 LinkedIn Smart Scheduler — Auto-Post Automation via Chrome DevTools Protocol

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![WebBridge](https://img.shields.io/badge/Kimi_WebBridge-daemon-orange)](https://kimi.ai)

> **Autonomously schedules LinkedIn posts on any custom future date and time using Chrome DevTools Protocol (CDP) + Kimi WebBridge — zero passwords, zero OAuth tokens, zero Selenium.**

---

## ✨ Features

1. **Schedule Any Custom Post (`schedule_post.py`)**:
   - Tell it **what to post**, **which date**, and **which time** — it handles the entire LinkedIn scheduling flow automatically.
   - **Interactive Mode**: Prompts you for date, time, and text (or file path).
   - **CLI Mode**: Run in a single command with `--date`, `--time`, and `--content` / `--file`.
   - **Flexible Parsers**: Supports dates like `10/12/2026`, `2026-10-12`, `Oct 15, 2026` and times like `6:00 PM`, `6pm`, `18:00`.

2. **11-Day Technical Campaign Scheduler (`linkedin_scheduler.py`)**:
   - Auto-reads live LinkedIn queue before scheduling.
   - Skips dates that are already queued — zero duplicates.
   - Schedules missing showcase posts at their designated dates.
   - Generates an end-of-run pass/fail verification table.

---

## 🏗️ Architecture

```
schedule_post.py  /  linkedin_scheduler.py
│
├── Step 1: Navigate to LinkedIn Feed
├── Step 2: Open "Start a post" compose dialog
├── Step 3: Inject post content via CDP fill() + execCommand fallback
├── Step 4: Click clock button (svg#clock-medium)
├── Step 5: Set Date on data-testid="date-picker-input" (React Native Setter)
├── Step 6: Set Time on data-testid="time-picker-input" (React Native Setter)
├── Step 7: Click "Confirm" in schedule dialog
└── Step 8: Click "Schedule" button (MouseEvent + native click)
```

### Why React Native Setter?

LinkedIn's date and time pickers are React-controlled inputs. Setting `.value` directly does not trigger React's internal state machine, leaving the Confirm button disabled. This tool uses React-aware property descriptors:

```python
nativeSetter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set
nativeSetter.call(input, '10/10/2026')
input.dispatchEvent(new Event('input', { bubbles: true }))
input.dispatchEvent(new Event('change', { bubbles: true }))
input.dispatchEvent(new Event('blur', { bubbles: true }))
```

---

## 🚀 Quick Start

### 1. Prerequisites

- **Kimi WebBridge** daemon running on `http://127.0.0.1:10086`  
  (Session name: `mail-cross-verify`)  
- Chrome browser open and **logged into LinkedIn**  
- Python 3.8+ (stdlib only — zero pip dependencies)

### 2. Schedule Any Custom Post

#### Option A: Interactive Mode (Recommended)
Simply run:
```bash
python schedule_post.py
```
It will prompt you:
```
📅 Enter target date (e.g. 10/10/2026 or Oct 10, 2026): 10/15/2026
⏰ Enter target time (e.g. 6:00 PM, 18:00) [Default: 12:00 PM]: 6:00 PM
📝 Choose how to provide post content:
   [1] Type / paste text directly here
   [2] Load text from a file (e.g. post.txt)
```

#### Option B: One-Liner CLI Arguments
```bash
# Pass text directly:
python schedule_post.py --date "10/15/2026" --time "6:00 PM" --text "Shipping something new today! 🚀"

# Or load from a file:
python schedule_post.py --date "10/15/2026" --time "6:00 PM" --file "my_post.txt"
```

### 3. Run the Automated 11-Day Campaign
```bash
python linkedin_scheduler.py
```

---

## 📅 Campaign Schedule (Sep 28 – Oct 10, 2026)

| Day | Date | Time | Repo / Topic |
|-----|------|------|--------------|
| 1 | Sep 28 | 12:00 PM | [AUTO-MATIC-MAIL-AGENT-](https://github.com/roshan-pixel/AUTO-MATIC-MAIL-AGENT-) |
| 2 | Sep 29 | 12:00 PM | [WinClaw](https://github.com/roshan-pixel/winclaw) |
| 3 | Sep 30 | 12:00 PM | [Hermes WhatsApp AI Agent on GCP VM](https://github.com/roshan-pixel/-Hermes-WhatsApp-AI-Agent-on-Google-Cloud-VM) |
| 4 | Oct 1  | 12:00 PM | [-ledger_web](https://github.com/roshan-pixel/-ledger_web) |
| 5 | Oct 2  | 12:00 PM | [WhatsApp-Web-Session-to-Google-Sheets](https://github.com/roshan-pixel/WhatsApp-Web-Session-to-Google-Sheets-Automation-Bot) |
| 6 | Oct 3  | 12:00 PM | [Asclepius-Portal-Synchronizer](https://github.com/roshan-pixel/Asclepius-Wellness-Portal-to-Google-Sheets-Synchronizer-MLM-Ledger) |
| 7 | Oct 4  | 12:00 PM | [TODOBAR](https://github.com/roshan-pixel/TODOBAR----DSKTOP----NPM) |
| 8 | Oct 5  | 12:00 PM | [linkedin-post-scraper-json](https://github.com/roshan-pixel/linkedin-post-scraper-json) |
| 9 | Oct 6  | 12:00 PM | [Local-Spending](https://github.com/roshan-pixel/Local-Spending) |
| 10 | Oct 7 | 12:00 PM | [Linked--in-automation-](https://github.com/roshan-pixel/Linked--in-automation-) |
| 11 | Oct 10 | 06:00 PM | **10-Day Technical Showcase Grand Finale & Complete Recap** |

---

## 📂 Repository Structure

| File | Purpose |
|---|---|
| `schedule_post.py` | **Custom Post Scheduler** — interactive prompt & CLI for any post text, date & time |
| `linkedin_scheduler.py` | **Full Campaign Scheduler** — auto-detects queue, skips duplicates, schedules 11 posts |
| `schedule_oct10.py` | Dedicated standalone script for Saturday Oct 10 at 6:00 PM recap |
| `post_now.py` | Immediate post dispatcher (posts right now, no schedule) |
| `run_full_schedule.py` | 10-day batch scheduler (calendar month nav engine) |
| `schedule_remaining_direct.py` | Direct date-input scheduler for Days 5/6/10 |

---

## 👤 Author

**Roshan Singh** — AI Security Researcher & Red Teamer  
[LinkedIn](https://linkedin.com/in/roshan-pixel) · [GitHub](https://github.com/roshan-pixel)

---

*Built with ❤️ using Chrome DevTools Protocol & Kimi WebBridge — zero passwords, zero OAuth tokens, zero Selenium.*
