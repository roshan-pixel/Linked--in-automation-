"""
================================================================================
🚀 LINKEDIN 10-DAY SEQUENTIAL SCHEDULER (ROCK-SOLID CALENDAR ENGINE)
================================================================================
Schedules the 10-day technical GitHub showcase for @roshan-pixel across
10 distinct dates from September 28 to October 7, 2026.

Uses Chrome DevTools Protocol & Kimi WebBridge with Next-Month Navigation
and verified active day targeting.
================================================================================
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True)

import json
import urllib.request
import time

BRIDGE_URL   = "http://127.0.0.1:10086/command"
SESSION_NAME = "mail-cross-verify"

QUEUE = [
    {
        "day": 1,
        "month": "September",
        "day_num": "28",
        "title": "AUTO-MATIC-MAIL-AGENT- (Autonomous CDP Webmail Engine)",
        "already_scheduled": True, # Verified scheduled for Sep 28
        "content": (
            "🚀 Just released AUTO-MATIC-MAIL-AGENT — an autonomous browser-driven email dispatch engine "
            "powered by Chrome DevTools Protocol (CDP) & Kimi WebBridge!\n\n"
            "Traditional email automation relies on SMTP passwords or OAuth apps that get revoked. "
            "AUTO-MATIC-MAIL-AGENT borrows your active, authenticated webmail session directly.\n\n"
            "🔑 Engineering Highlights:\n"
            "• CDP Recipient Tokenization: Injects To/Cc recipients and commits chips natively via Input.dispatchKeyEvent (Enter) — zero red invalidPill errors.\n"
            "• React & TrustedHTML Resilient: Native WebBridge fill() bypasses synthetic event sandboxes and strict CSP policies.\n"
            "• Zero-Leakage Privacy Guard: Built-in DataSanitizer with real-time Luhn algorithm checksum blocks PAN cards, CVVs, and SSH keys before any packet leaves.\n"
            "• Dual-Provider Support: Verified end-to-end for Microsoft Outlook Web & Google Gmail Web.\n"
            "• 16/16 pytest test suite with complete Mermaid sequence diagrams & architecture docs.\n\n"
            "🔗 GitHub: https://github.com/roshan-pixel/AUTO-MATIC-MAIL-AGENT-\n\n"
            "#Python #Automation #CDP #DevTools #EmailAutomation #WebBridge #OpenSource #BuildInPublic"
        )
    },
    {
        "day": 2,
        "month": "September",
        "day_num": "29",
        "title": "WinClaw (Model Context Protocol AI Automation Framework)",
        "already_scheduled": True,
        "content": (
            "🤖 Giving LLMs hands and feet without giving them keys to the kingdom 🦞⚡\n\n"
            "I built WinClaw to bridge foundation models (Claude, DeepSeek, Ollama) directly to native Windows environments "
            "using the Model Context Protocol (MCP) standard.\n\n"
            "🔑 Core Architecture & Capabilities:\n"
            "• 22+ Native Tools: Screenshot capture, PowerShell execution, window management, process inspection, and browser automation.\n"
            "• Security First: Strict JSON schema validation on every tool call prevents prompt injection from executing unconstrained shell actions.\n"
            "• Protocol Native: Built strictly on the open MCP standard for seamless plug-and-play with any MCP client.\n"
            "• Hybrid TypeScript & Python core designed for minimal latency and rock-solid tool dispatch.\n\n"
            "🔗 GitHub: https://github.com/roshan-pixel/winclaw\n\n"
            "#WinClaw #ModelContextProtocol #MCP #AISecurity #AgenticAI #Python #TypeScript #OpenSource"
        )
    },
    {
        "day": 3,
        "month": "September",
        "day_num": "30",
        "title": "Hermes WhatsApp AI Agent deployed on Google Cloud Platform (GCP) VM",
        "already_scheduled": True,
        "content": (
            "☁️ Deploying an autonomous WhatsApp AI conversational agent on Google Cloud VM with 99.9% uptime 💬⚡\n\n"
            "Running AI agents on messaging platforms requires solving three big infrastructure problems:\n"
            "1️⃣ Persistent session keeping across unexpected network drops\n"
            "2️⃣ Real-time streaming response generation without blocking incoming webhooks\n"
            "3️⃣ Stateless failover & daemon recovery\n\n"
            "Inside the Hermes deployment on GCP Compute Engine:\n"
            "• Background process manager with healthcheck heartbeats\n"
            "• Isolated context buffers to keep conversational memory sharp and relevant\n"
            "• Zero-downtime log rotation & error telemetry\n\n"
            "🔗 GitHub: https://github.com/roshan-pixel/-Hermes-WhatsApp-AI-Agent-on-Google-Cloud-VM\n\n"
            "#GoogleCloud #GCP #DevOps #WhatsAppAI #AIAgents #CloudEngineering #FullStack #SystemDesign"
        )
    },
    {
        "day": 4,
        "month": "October",
        "day_num": "1",
        "title": "Ledger God Mode Web App (-ledger_web)",
        "already_scheduled": True, # Verified scheduled for Oct 1
        "content": (
            "📊 From manual billing chaos to an automated billing, inventory & C&F portal sync engine ⚡\n\n"
            "High-volume wholesale and retail operations often struggle with slow invoicing, mismatched stock, and manual reconciliation. "
            "I built Ledger God Mode Web App (-ledger_web) to solve this end-to-end:\n\n"
            "✨ What it handles:\n"
            "• Lightning-Fast Invoicing: Cloud-ready invoice generator with auto tax & discount computation.\n"
            "• Real-Time Inventory Control: Live stock level tracking that syncs instantly upon order fulfillment.\n"
            "• C&F Portal Synchronizer: Seamless synchronization with clearing and forwarding portals.\n"
            "• Built for operational speed and zero downtime.\n\n"
            "🔗 GitHub: https://github.com/roshan-pixel/-ledger_web\n\n"
            "#WebDevelopment #FinTech #FullStack #InventoryManagement #BillingApp #SoftwareEngineering #Cloud"
        )
    },
    {
        "day": 5,
        "month": "October",
        "day_num": "2",
        "title": "WhatsApp Web to Google Sheets Automation Bot",
        "already_scheduled": False,
        "content": (
            "📈 Turn your WhatsApp chat sessions into an instant, zero-database CRM in Google Sheets 💬📊\n\n"
            "Small businesses and indie hackers don't need heavyweight $100/mo CRMs just to log customer inquiries and orders. "
            "This bot bridges WhatsApp Web directly to Google Sheets in real-time.\n\n"
            "⚙️ How it works:\n"
            "• Intercepts incoming messages and metadata via browser session hooks\n"
            "• Automatically appends contact details, timestamps, message content, and tags to Google Sheets via API\n"
            "• Session persistence prevents repeated QR code re-authentications\n"
            "• Zero third-party middleware — clean, direct, and completely customizable.\n\n"
            "🔗 GitHub: https://github.com/roshan-pixel/WhatsApp-Web-Session-to-Google-Sheets-Automation-Bot\n\n"
            "#Automation #GoogleSheetsAPI #WhatsAppAutomation #Python #IndieHacker #Productivity #NoCode"
        )
    },
    {
        "day": 6,
        "month": "October",
        "day_num": "3",
        "title": "Asclepius Portal to Google Sheets Synchronizer & MLM Ledger",
        "already_scheduled": False,
        "content": (
            "🔄 Synchronizing complex authenticated enterprise portals to Google Sheets at scale 📦⚡\n\n"
            "Enterprise portals with multi-tiered payout structures and distributor hierarchies are notoriously tricky to extract data from. "
            "I engineered an automated ETL synchronizer that extracts, normalizes, and syncs live records:\n\n"
            "🔑 Engineering Highlights:\n"
            "• Multi-step authenticated session traversal with cookie and token caching\n"
            "• Resilient DOM parsers handling pagination and dynamic tables\n"
            "• Automated payout calculations, incentive tracking, and ledger reconciliation in Google Sheets\n"
            "• Exponential backoff & rate-limiting to ensure uninterrupted sync runs\n\n"
            "🔗 GitHub: https://github.com/roshan-pixel/Asclepius-Wellness-Portal-to-Google-Sheets-Synchronizer-MLM-Ledger\n\n"
            "#DataEngineering #ETL #WebScraping #Python #Automation #DataPipelines #Analytics"
        )
    },
    {
        "day": 7,
        "month": "October",
        "day_num": "4",
        "title": "TODOBAR — Floating Desktop Productivity Bar on NPM",
        "already_scheduled": True,
        "content": (
            "💻 Why I built a floating, keyboard-first desktop task bar and published it to NPM ⏱️✨\n\n"
            "Full-screen task managers break your flow. Browser tabs get buried. Sticky notes clutter your workspace.\n\n"
            "TODOBAR is a minimal, distraction-free desktop task utility that lives right at the edge of your screen:\n\n"
            "🚀 What makes it tick:\n"
            "• Global Hotkey Toggle: Press a shortcut, jot down a task, press Enter, get back to coding in under 2 seconds.\n"
            "• Offline-First: Stores tasks locally with zero cloud dependencies or lag.\n"
            "• Lightweight & Native: TypeScript & Electron engine designed with negligible RAM footprint.\n"
            "• Installable in seconds directly via NPM.\n\n"
            "🔗 GitHub: https://github.com/roshan-pixel/TODOBAR----DSKTOP----NPM\n\n"
            "#TypeScript #NPM #DesktopApp #DeveloperTools #Productivity #UIUX #OpenSource"
        )
    },
    {
        "day": 8,
        "month": "October",
        "day_num": "5",
        "title": "LinkedIn Post Scraper (Structured JSON Telemetry)",
        "already_scheduled": True,
        "content": (
            "🔍 Extracting structured telemetry from infinite-scroll web feeds using Python 📊🕸️\n\n"
            "Scraping dynamic modern web feeds like LinkedIn requires overcoming DOM virtualization, lazy loading, and rate-limiting.\n\n"
            "My open-source `linkedin-post-scraper-json` extracts full feed telemetry cleanly:\n\n"
            "⚙️ Technical Capabilities:\n"
            "• Virtual Scroll Observer: Progressively triggers dynamic rendering without triggering bot detection traps.\n"
            "• Rich Metadata Extraction: Captures author profile info, post text, embedded links, reaction counts, and comment distributions.\n"
            "• Clean JSON Output: Ready for sentiment analysis, competitive intelligence, and content strategy modeling.\n\n"
            "🔗 GitHub: https://github.com/roshan-pixel/linkedin-post-scraper-json\n\n"
            "#WebScraping #Python #DataScience #DataExtraction #CompetitiveIntel #SocialMediaAnalytics"
        )
    },
    {
        "day": 9,
        "month": "October",
        "day_num": "6",
        "title": "Local-Spending (Privacy-Preserving Personal Finance Analytics)",
        "already_scheduled": False,
        "content": (
            "💳 Your financial data belongs to you — not third-party SaaS cloud trackers 🔒📉\n\n"
            "Most budgeting apps require linking bank credentials to cloud servers where data is mined or exposed in breaches. "
            "I built `Local-Spending` as an offline-first financial analytics engine:\n\n"
            "🛡️ Core Privacy & Engineering Principles:\n"
            "• 100% Local Storage: Zero network calls, zero analytics trackers, zero cloud leakage.\n"
            "• Automated Categorization: Categorizes transactions, tracks monthly variance, and detects recurring subscriptions.\n"
            "• Clean Dashboards: Fast visual reporting on expense breakdowns without sacrificing data sovereignty.\n\n"
            "🔗 GitHub: https://github.com/roshan-pixel/Local-Spending\n\n"
            "#PersonalFinance #DataPrivacy #LocalFirst #Python #FinTech #Security #OpenSource"
        )
    },
    {
        "day": 10,
        "month": "October",
        "day_num": "7",
        "title": "LinkedIn 30-Day Post Automation Framework (CDP & WebBridge)",
        "already_scheduled": False,
        "content": (
            "📅 The engineering behind 30-day automated LinkedIn post scheduling 🚀⚡\n\n"
            "Scheduling posts programmatically on LinkedIn is notoriously difficult because of their nested `#interop-outlet` Shadow DOM "
            "and React-controlled calendar inputs.\n\n"
            "My open-source `Linked--in-automation-` framework solves this with Chrome DevTools Protocol (CDP):\n\n"
            "💡 How It Works Under The Hood:\n"
            "• CDP Pointer Precision: Dispatches native mouse coordinates directly to calendar day buttons inside Shadow DOM.\n"
            "• Active Session Borrowing: Connects via Kimi WebBridge daemon — uses existing logged-in browser cookies with zero password storage.\n"
            "• Continuous Multi-Day Queue: Schedules consecutive future dates at customizable time slots (e.g. 12:00 PM).\n"
            "• Complete resilience against DOM updates.\n\n"
            "🔗 GitHub: https://github.com/roshan-pixel/Linked--in-automation-\n\n"
            "#BrowserAutomation #CDP #ChromeDevTools #LinkedInAutomation #Python #OpenSource #BuildInPublic"
        )
    }
]

def cmd(action, args=None):
    payload = json.dumps({"action": action, "session": SESSION_NAME, "args": args or {}}).encode("utf-8")
    req = urllib.request.Request(BRIDGE_URL, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=35) as r:
        return json.loads(r.read().decode("utf-8"))

def wait_for_condition(eval_expr, max_seconds=10.0, step=0.5):
    start = time.time()
    while time.time() - start < max_seconds:
        res = cmd("evaluate", {"code": eval_expr})
        if res.get("data", {}).get("value"):
            return True
        time.sleep(step)
    return False

def schedule_single_post(post):
    day_num = post["day"]
    target_month = post["month"]
    target_day = post["day_num"]
    title = post["title"]
    content = post["content"]
    date_str = f"{target_month} {target_day}, 2026"

    print("\n" + "=" * 65, flush=True)
    print(f"  📅 SCHEDULING DAY {day_num}/10: {date_str}", flush=True)
    print(f"  🎯 {title}", flush=True)
    print("=" * 65, flush=True)

    # 1. Feed navigation
    print("  [1/7] Navigating to feed...", flush=True)
    cmd("navigate", {"url": "https://www.linkedin.com/feed/"})
    time.sleep(5.0)

    # 2. Click Start a post
    print("  [2/7] Opening 'Start a post'...", flush=True)
    for attempt in range(4):
        cmd("evaluate", {"code": """(() => {
            const btn = Array.from(document.querySelectorAll('button, div[role="button"]')).find(e => (e.innerText||'').trim() === 'Start a post');
            if (btn) btn.click();
        })()"""})
        if wait_for_condition("Boolean(document.querySelector('[role=textbox]') || document.querySelector('div[contenteditable=\"true\"]'))", 4.0):
            break
        time.sleep(1.5)

    time.sleep(1.5)

    # 3. Inject content
    print("  [3/7] Injecting post text...", flush=True)
    wait_for_condition("Boolean(document.querySelector('[role=textbox]') || document.querySelector('div[contenteditable=\"true\"]'))", 8.0)
    time.sleep(1.0)
    cmd("evaluate", {"code": """(() => {
        const el = document.querySelector('[role="textbox"]') || document.querySelector('div[contenteditable="true"]');
        if (el) el.focus();
    })()"""})
    time.sleep(0.5)
    fill_ok = False
    for selector in ["[role=textbox]", ".ql-editor", "div[contenteditable=true]"]:
        res = cmd("fill", {"selector": selector, "value": content})
        if res.get("ok"):
            fill_ok = True
            print(f"      ✓ Injected via {selector}", flush=True)
            break
        time.sleep(0.8)

    if not fill_ok:
        eval_fill = cmd("evaluate", {"code": f"""(() => {{
            const el = document.querySelector('[role="textbox"]') || document.querySelector('div.ql-editor') || document.querySelector('div[contenteditable="true"]');
            if (el) {{
                el.focus();
                document.execCommand('selectAll', false, null);
                document.execCommand('insertText', false, {json.dumps(content)});
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                return true;
            }}
            return false;
        }})()"""})
        if eval_fill.get("data", {}).get("value"):
            fill_ok = True
            print("      ✓ Injected via execCommand fallback", flush=True)

    if not fill_ok:
        print("  ❌ Failed to inject text", flush=True)
        return False
    time.sleep(1.5)

    # 4. Open Schedule modal (click clock)
    print("  [4/7] Opening Schedule modal...", flush=True)
    cmd("evaluate", {"code": """(() => {
        const clock = document.querySelector('svg#clock-medium');
        if (clock) clock.closest('a, button').click();
    })()"""})
    wait_for_condition("Boolean(Array.from(document.querySelectorAll('button')).find(b => (b.getAttribute('aria-label')||'').includes('calendar') || (b.innerText||'').includes('calendar') || b.querySelector('svg[id*=\"calendar\"]')))", 8.0)
    time.sleep(1.0)

    # 5. Open Calendar
    print("  [5/7] Opening calendar picker...", flush=True)
    cmd("evaluate", {"code": """(() => {
        const cal = Array.from(document.querySelectorAll('button')).find(b => (b.getAttribute('aria-label')||'').includes('calendar') || (b.innerText||'').includes('calendar') || b.querySelector('svg[id*=\"calendar\"]'));
        if (cal) cal.click();
    })()"""})
    wait_for_condition("Boolean(Array.from(document.querySelectorAll('button')).find(b => (b.getAttribute('aria-label')||'').includes('Select ')))", 8.0)
    time.sleep(1.0)

    # 6. Navigate month if needed and select date
    print(f"  [6/7] Setting calendar to {target_month} and picking day {target_day}...", flush=True)
    for m_attempt in range(5):
        header_res = cmd("evaluate", {"code": f"""(() => {{
            const yearBtn = Array.from(document.querySelectorAll('button')).find(b => (b.getAttribute('aria-label')||'').includes('year'));
            const text = yearBtn ? yearBtn.innerText : '';
            if ('{target_month}' === 'October' && text.includes('September')) {{
                const nextBtn = Array.from(document.querySelectorAll('button')).find(b => b.getAttribute('aria-label') === 'Next month');
                if (nextBtn) nextBtn.click();
                return 'clicked_next';
            }}
            if ('{target_month}' === 'September' && text.includes('October')) {{
                const prevBtn = Array.from(document.querySelectorAll('button')).find(b => b.getAttribute('aria-label') === 'Previous month');
                if (prevBtn) prevBtn.click();
                return 'clicked_prev';
            }}
            if (text.includes('{target_month}')) return 'ready';
            return 'waiting';
        }})()"""})
        val = header_res.get("data", {}).get("value")
        if val == 'ready':
            break
        time.sleep(1.0)

    full_label = f"Select {target_month} {target_day}, 2026"
    wait_for_condition(f"Boolean(Array.from(document.querySelectorAll('button')).find(b => b.getAttribute('aria-label') === '{full_label}' && !b.disabled))", 8.0)

    # Click the specific enabled day button
    day_res = cmd("evaluate", {"code": f"""(() => {{
        const fullLabel = '{full_label}';
        const dayBtn = Array.from(document.querySelectorAll('button')).find(b => 
            b.getAttribute('aria-label') === fullLabel && !b.disabled
        );
        if (dayBtn) {{
            dayBtn.click();
            return 'clicked: ' + fullLabel;
        }}
        return 'not_found';
    }})()"""})
    
    val = day_res.get("data", {}).get("value")
    if val == 'not_found':
        print(f"  ❌ Day button for '{date_str}' not found or disabled!", flush=True)
        return False
    print(f"      ✓ {val}", flush=True)
    time.sleep(1.5)

    # 7. Confirm in schedule dialog
    print("  [7/7] Confirming and scheduling...", flush=True)
    cmd("evaluate", {"code": """(() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => (b.innerText||'').trim() === 'Confirm' && b.offsetParent !== null);
        if (btn) btn.click();
    })()"""})
    time.sleep(2.0)

    # Click main Schedule button
    sched_ready = wait_for_condition("Boolean(Array.from(document.querySelectorAll('button')).find(b => (b.innerText||'').trim() === 'Schedule' && b.offsetParent !== null))", 8.0)
    if not sched_ready:
        print("  ❌ Schedule button never appeared after Confirm", flush=True)
        return False

    cmd("evaluate", {"code": """(() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => (b.innerText||'').trim() === 'Schedule' && b.offsetParent !== null);
        if (btn) btn.click();
    })()"""})
    print("      ✓ Clicked Schedule button", flush=True)

    time.sleep(4.0)
    print(f"  🎉 SUCCESS: Day {day_num} scheduled for {date_str} on LinkedIn!", flush=True)
    return True

def main():
    print("=" * 65, flush=True)
    print("  🚀 LINKEDIN 10-DAY SEQUENTIAL POST SCHEDULER", flush=True)
    print("=" * 65, flush=True)

    success_count = 0
    for p in QUEUE:
        if p.get("already_scheduled"):
            print(f"⏭️  Day {p['day']}: {p['month']} {p['day_num']}, 2026 — Already verified scheduled, skipping.", flush=True)
            success_count += 1
            continue
        try:
            ok = schedule_single_post(p)
            if ok:
                success_count += 1
                p["already_scheduled"] = True
            time.sleep(3.0)
        except Exception as e:
            print(f"  ❌ Error on Day {p['day']}: {e}", flush=True)
            time.sleep(3.0)

    print("\n" + "=" * 65, flush=True)
    print(f"  🏁 BATCH FINISHED: {success_count}/10 posts queued on LinkedIn!", flush=True)
    print("=" * 65, flush=True)

if __name__ == "__main__":
    main()
