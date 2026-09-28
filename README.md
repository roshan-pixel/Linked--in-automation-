# 🤖 LinkedIn Smart Scheduler — Auto-Post Automation via Chrome DevTools Protocol

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![WebBridge](https://img.shields.io/badge/Kimi_WebBridge-daemon-orange)](https://kimi.ai)

> **Autonomously schedules LinkedIn posts on correct future dates using Chrome DevTools Protocol (CDP) + Kimi WebBridge — no Selenium, no Playwright, no OAuth tokens.**

---

## ✨ What It Does

`linkedin_scheduler.py` is a single self-contained Python script that:

1. **Auto-detects** the current LinkedIn scheduled-posts queue (reads live from LinkedIn)  
2. **Skips** dates that are already queued — zero duplicates  
3. **Schedules** only the missing posts at the correct target dates  
4. **Verifies** the final queue and prints a pass/fail table  
5. **Retries** each step up to 3 times before giving up  

---

## 🏗️ Architecture

```
linkedin_scheduler.py
│
├── fetch_scheduled_queue()    ← reads live LinkedIn scheduled list
├── schedule_post(post)        ← full scheduling flow per post
│   ├── navigate feed
│   ├── open compose modal
│   ├── inject post text (fill + execCommand fallback)
│   ├── open clock / schedule dialog
│   ├── set date via React native property setter (MM/DD/YYYY)
│   ├── set time (default: 12:00 PM or custom post_time)
│   └── Confirm → Schedule
└── verify_queue()             ← re-reads queue, prints status table
```

### Why React Native Setter?

LinkedIn's date picker is a React-controlled `<input>`. Setting `.value` directly doesn't trigger React's internal state — the Confirm button stays disabled. The fix:

```python
# React-aware value injection (bypasses synthetic event sandbox)
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
- Python 3.8+ (stdlib only — no pip installs needed)

### 2. Run

To run the full campaign:
```bash
python linkedin_scheduler.py
```

To schedule a dedicated single post (e.g. Oct 10 at 6:00 PM):
```bash
python schedule_oct10.py
```

The script will:
- Print which dates are already scheduled (skipped)
- Print which dates it's scheduling now
- Show a final ✅/❌ verification table

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

## ⚙️ Configuration

Edit the top of `linkedin_scheduler.py`:

```python
BRIDGE_URL    = "http://127.0.0.1:10086/command"  # WebBridge endpoint
SESSION_NAME  = "mail-cross-verify"               # browser session name
MAX_STEP_RETRIES = 3                              # retries per step
POST_TIME     = "12:00 PM"                        # default post time
```

To add/edit posts, modify the `CAMPAIGN` list — each entry has:

```python
{
    "day":        11,              # display only
    "date_input": "10/10/2026",   # MM/DD/YYYY — fed to React input
    "date_label": "Oct 10, 2026", # human-readable label
    "post_time":  "06:00 PM",     # optional post time override
    "title":      "...",          # log only
    "content":    "...",          # full post text
}
```

---

## 🐛 Known Edge Cases Solved

| Problem | Solution |
|---|---|
| Calendar stays on September, October dates disabled | React native setter bypasses calendar entirely |
| Multiple posts landing on same date | `fetch_scheduled_queue()` reads live queue first; duplicates skipped |
| WebBridge 502 transient error | `MAX_STEP_RETRIES = 3` retries each step |
| React event sandbox blocks `.value =` | `Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set` |
| Custom time per post (e.g. 6:00 PM) | Supported via `post_time` override and native setter on time picker |
| Session expired | Script navigates feed and checks URL; fails fast with clear error |

---

## 📂 Files

| File | Purpose |
|---|---|
| `linkedin_scheduler.py` | **Main script** — smart auto-detect scheduler for 11-post campaign |
| `schedule_oct10.py` | Dedicated standalone scheduler for Oct 10, 2026 at 6:00 PM |
| `linkedin_automation.py` | Legacy engine (CDP mouse click approach) |
| `run_full_schedule.py` | 10-day batch scheduler (calendar nav approach) |
| `schedule_remaining_direct.py` | Direct date-input scheduler for Days 5/6/10 |

---

## 👤 Author

**Roshan Singh** — AI Security Researcher & Red Teamer  
[LinkedIn](https://linkedin.com/in/roshan-pixel) · [GitHub](https://github.com/roshan-pixel)

---

*Built with ❤️ using Chrome DevTools Protocol & Kimi WebBridge — zero passwords, zero OAuth tokens, zero Selenium.*
