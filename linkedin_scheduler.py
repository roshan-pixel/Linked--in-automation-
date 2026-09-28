"""
================================================================================
🚀 LINKEDIN SMART SCHEDULER — AUTO-DETECT & POST ON CORRECT DATES
================================================================================
Author  : roshan-pixel
Repo    : https://github.com/roshan-pixel/Linked--in-automation-
Bridge  : Kimi WebBridge daemon at http://127.0.0.1:10086
Session : mail-cross-verify

HOW IT WORKS
────────────
1. Opens the LinkedIn scheduled-posts list (via /sharing/compose)
2. Parses every "Posting Mon/Tue/… at HH:MM AM/PM" line to know what's
   already queued (date + preview text).
3. For each of the 10 planned posts, checks if the target date already has
   a matching post in the queue — skips if yes.
4. For any missing post it runs the full flow:
      navigate → start post → inject text → open clock → set date
      via React native-setter on data-testid="date-picker-input" → Confirm → Schedule
5. After scheduling, re-reads the queue and prints a final verification table.

DATE/TIME
─────────
Default post time : 12:00 PM  (noon IST)
Format for input  : MM/DD/YYYY  (e.g. "10/02/2026")

RETRY
─────
Each step retries up to MAX_STEP_RETRIES times before giving up on a post.
================================================================================
"""

import sys, json, time, re, urllib.request
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True)

# ──────────────────────────────────────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────────────────────────────────────
BRIDGE_URL       = "http://127.0.0.1:10086/command"
SESSION_NAME     = "mail-cross-verify"
MAX_STEP_RETRIES = 3
POST_TIME        = "12:00 PM"   # time to set for every post

# ──────────────────────────────────────────────────────────────────────────────
# 10-DAY CAMPAIGN  (date_input = MM/DD/YYYY, date_label = human-readable)
# ──────────────────────────────────────────────────────────────────────────────
CAMPAIGN = [
    {
        "day": 1,
        "date_input": "09/28/2026",
        "date_label": "Sep 28, 2026",
        "title": "AUTO-MATIC-MAIL-AGENT- (Autonomous CDP Webmail Engine)",
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
        ),
    },
    {
        "day": 2,
        "date_input": "09/29/2026",
        "date_label": "Sep 29, 2026",
        "title": "WinClaw (Model Context Protocol AI Automation Framework)",
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
        ),
    },
    {
        "day": 3,
        "date_input": "09/30/2026",
        "date_label": "Sep 30, 2026",
        "title": "Hermes WhatsApp AI Agent on GCP VM",
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
        ),
    },
    {
        "day": 4,
        "date_input": "10/01/2026",
        "date_label": "Oct 1, 2026",
        "title": "Ledger God Mode Web App (-ledger_web)",
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
        ),
    },
    {
        "day": 5,
        "date_input": "10/02/2026",
        "date_label": "Oct 2, 2026",
        "title": "WhatsApp Web to Google Sheets Automation Bot",
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
        ),
    },
    {
        "day": 6,
        "date_input": "10/03/2026",
        "date_label": "Oct 3, 2026",
        "title": "Asclepius Portal to Google Sheets Synchronizer & MLM Ledger",
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
        ),
    },
    {
        "day": 7,
        "date_input": "10/04/2026",
        "date_label": "Oct 4, 2026",
        "title": "TODOBAR — Floating Desktop Productivity Bar on NPM",
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
        ),
    },
    {
        "day": 8,
        "date_input": "10/05/2026",
        "date_label": "Oct 5, 2026",
        "title": "LinkedIn Post Scraper (Structured JSON Telemetry)",
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
        ),
    },
    {
        "day": 9,
        "date_input": "10/06/2026",
        "date_label": "Oct 6, 2026",
        "title": "Local-Spending (Privacy-Preserving Personal Finance Analytics)",
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
        ),
    },
    {
        "day": 10,
        "date_input": "10/07/2026",
        "date_label": "Oct 7, 2026",
        "title": "LinkedIn 30-Day Post Automation Framework (CDP & WebBridge)",
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
        ),
    },
    {
        "day": 11,
        "date_input": "10/10/2026",
        "date_label": "Oct 10, 2026",
        "post_time": "06:00 PM",
        "title": "10-Day Technical Showcase Grand Finale & Complete Recap",
        "content": (
            "🔐 10 days of shipping. 10 open-source projects. Here's what I built.\n\n"
            "Over the last 10 days I've been doing a deep-dive showcase of every repo I've shipped this year. "
            "From autonomous email agents to AI security frameworks — here's the full lineup:\n\n"
            "1️⃣ AUTO-MATIC-MAIL-AGENT — CDP-powered webmail automation\n"
            "2️⃣ WinClaw — MCP AI framework for Windows native tools\n"
            "3️⃣ Hermes — WhatsApp AI Agent on GCP VM\n"
            "4️⃣ -ledger_web — Billing, inventory & C&F portal sync\n"
            "5️⃣ WhatsApp-Web-to-Google-Sheets — Zero-database WhatsApp CRM\n"
            "6️⃣ Asclepius Portal Sync — Enterprise ETL to Google Sheets\n"
            "7️⃣ TODOBAR — Floating desktop task bar on NPM\n"
            "8️⃣ linkedin-post-scraper-json — Structured feed telemetry\n"
            "9️⃣ Local-Spending — Privacy-first personal finance analytics\n"
            "🔟 Linked--in-automation- — This entire automated campaign engine 🤖\n\n"
            "All 10 repos are open-source and linked in my profile.\n\n"
            "Which one would you actually use? Drop it in the comments 👇\n\n"
            "#OpenSource #BuildInPublic #Python #AI #SecurityResearch #GitHub #Automation"
        ),
    },
]

# ──────────────────────────────────────────────────────────────────────────────
# WEBBRIDGE HELPERS
# ──────────────────────────────────────────────────────────────────────────────
def cmd(action, args=None):
    payload = json.dumps({"action": action, "session": SESSION_NAME, "args": args or {}}).encode()
    req = urllib.request.Request(BRIDGE_URL, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read().decode())

def evaluate(code):
    return cmd("evaluate", {"code": code})

def val(res):
    """Extract the .data.value from a WebBridge response."""
    return res.get("data", {}).get("value")

def wait_for(js_expr, max_sec=12.0, step=0.5):
    """Poll until js_expr is truthy or timeout. Returns True/False."""
    deadline = time.time() + max_sec
    while time.time() < deadline:
        if val(evaluate(js_expr)):
            return True
        time.sleep(step)
    return False

# ──────────────────────────────────────────────────────────────────────────────
# STEP 1 — READ CURRENT SCHEDULED QUEUE
# ──────────────────────────────────────────────────────────────────────────────
def fetch_scheduled_queue():
    """
    Opens /sharing/compose, reads the left-panel scheduled list, returns
    a set of date strings found (e.g. {'Sep 28', 'Sep 29', 'Oct 1', ...}).
    Also returns raw 'Posting …' lines for logging.
    """
    print("\n📋 Fetching current LinkedIn scheduled queue...", flush=True)
    cmd("navigate", {"url": "https://www.linkedin.com/sharing/compose"})
    time.sleep(5)

    # Read body text — on this page the scheduled list sidebar IS rendered
    raw = val(evaluate("document.body.innerText")) or ""

    # Also click the Scheduled (N) tab if compose modal opened
    if "Scheduled (" in raw:
        # Try to click it to open the list view
        evaluate("""(() => {
            const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
            let n;
            while ((n = walker.nextNode())) {
                if (/^Scheduled \\(\\d+\\)$/.test(n.textContent.trim())) {
                    let el = n.parentElement;
                    for (let i = 0; i < 8; i++) {
                        if (!el) break;
                        if (['BUTTON','A'].includes(el.tagName) || el.getAttribute('role') === 'button') {
                            el.click(); return 'clicked';
                        }
                        el = el.parentElement;
                    }
                    n.parentElement && n.parentElement.click();
                    return 'clicked_parent';
                }
            }
            return 'not_found';
        })()""")
        time.sleep(3)
        raw = val(evaluate("document.body.innerText")) or ""

    # Parse all "Posting Mon, Oct 2, 2026 at 12:00 PM" style lines
    # Handles both formats LinkedIn uses:
    #   "Posting Mon, Sep 28, 2026 at 8:00 AM"
    #   "Posting at Mon, Sep 28, 7:45 AM"
    pattern = re.compile(
        r'Posting(?: at)?\s+(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun),?\s+'
        r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2})'
        r'(?:,\s*\d{4})?\s+at\s+[\d:]+\s+(?:AM|PM)',
        re.IGNORECASE
    )
    posting_lines = pattern.findall(raw)
    scheduled_dates = set()
    for line in posting_lines:
        # Normalize: "Sep 28" → "Sep 28", "Oct 2" → "Oct 2"
        m = re.search(r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2})', line)
        if m:
            scheduled_dates.add(m.group(1).strip())

    print(f"   Found {len(posting_lines)} existing scheduled posts:", flush=True)
    for s in sorted(scheduled_dates):
        print(f"     • {s}", flush=True)

    return scheduled_dates, posting_lines

# ──────────────────────────────────────────────────────────────────────────────
# DATE NORMALIZATION HELPER
# ──────────────────────────────────────────────────────────────────────────────
MONTH_SHORT = {
    "01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr",
    "05": "May", "06": "Jun", "07": "Jul", "08": "Aug",
    "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"
}

def date_input_to_short(date_input):
    """'10/02/2026' → 'Oct 2'"""
    parts = date_input.split("/")
    mon = MONTH_SHORT.get(parts[0], parts[0])
    day = str(int(parts[1]))   # strip leading zero
    return f"{mon} {day}"

# ──────────────────────────────────────────────────────────────────────────────
# STEP 2 — SCHEDULE ONE POST
# ──────────────────────────────────────────────────────────────────────────────
def schedule_post(post):
    day_num    = post["day"]
    date_input = post["date_input"]   # MM/DD/YYYY
    date_label = post["date_label"]   # human-readable for logging
    post_time  = post.get("post_time", POST_TIME)
    title      = post["title"]
    content    = post["content"]

    print(f"\n{'='*65}", flush=True)
    print(f"  📅 DAY {day_num} → {date_label} at {post_time}  |  {title}", flush=True)
    print(f"{'='*65}", flush=True)

    # ── 1. Navigate to LinkedIn feed ──────────────────────────────────────────
    print("  [1/6] Navigating to feed...", flush=True)
    for attempt in range(MAX_STEP_RETRIES):
        cmd("navigate", {"url": "https://www.linkedin.com/feed/"})
        time.sleep(5)
        url = val(evaluate("window.location.href")) or ""
        if "linkedin.com/feed" in url or "linkedin.com" in url:
            break
        print(f"      ⚠ Retry {attempt+1}...", flush=True)
    else:
        print("  ❌ Could not load LinkedIn feed", flush=True)
        return False

    # ── 2. Open compose modal ─────────────────────────────────────────────────
    print("  [2/6] Opening 'Start a post'...", flush=True)
    opened = False
    for attempt in range(MAX_STEP_RETRIES):
        evaluate("""(() => {
            const btn = Array.from(document.querySelectorAll('button, div[role="button"]'))
                .find(e => (e.innerText||'').trim() === 'Start a post');
            if (btn) btn.click();
        })()""")
        if wait_for(
            "Boolean(document.querySelector('[role=textbox]') || document.querySelector('div[contenteditable=\"true\"]'))",
            max_sec=6
        ):
            opened = True
            break
        time.sleep(2)
    if not opened:
        print("  ❌ Compose modal never opened", flush=True)
        return False
    time.sleep(1.5)

    # ── 3. Inject post text ───────────────────────────────────────────────────
    print("  [3/6] Injecting post content...", flush=True)
    wait_for(
        "Boolean(document.querySelector('[role=textbox]') || document.querySelector('div[contenteditable=\"true\"]'))",
        max_sec=8
    )
    evaluate("""(() => {
        const el = document.querySelector('[role="textbox"]') || document.querySelector('div[contenteditable="true"]');
        if (el) el.focus();
    })()""")
    time.sleep(0.5)

    fill_ok = False
    for selector in ["[role=textbox]", ".ql-editor", "div[contenteditable=true]"]:
        res = cmd("fill", {"selector": selector, "value": content})
        if res.get("ok"):
            fill_ok = True
            print(f"      ✓ Filled via {selector}", flush=True)
            break
        time.sleep(0.8)

    if not fill_ok:
        # execCommand fallback
        res2 = evaluate(f"""(() => {{
            const el = document.querySelector('[role="textbox"]')
                    || document.querySelector('div.ql-editor')
                    || document.querySelector('div[contenteditable="true"]');
            if (!el) return false;
            el.focus();
            document.execCommand('selectAll', false, null);
            document.execCommand('insertText', false, {json.dumps(content)});
            el.dispatchEvent(new Event('input', {{ bubbles: true }}));
            return true;
        }})()""")
        if val(res2):
            fill_ok = True
            print("      ✓ Filled via execCommand fallback", flush=True)

    if not fill_ok:
        print("  ❌ Could not inject post text", flush=True)
        return False
    time.sleep(1.5)

    # ── 4. Open Schedule modal (click clock icon) ─────────────────────────────
    print("  [4/6] Opening schedule dialog...", flush=True)
    clock_opened = False
    for attempt in range(MAX_STEP_RETRIES):
        evaluate("""(() => {
            const clock = document.querySelector('svg#clock-medium');
            if (clock) {
                const parent = clock.closest('a, button');
                if (parent) { parent.click(); return; }
            }
            const all = Array.from(document.querySelectorAll('button, a'));
            const btn = all.find(b => b.querySelector('svg#clock-medium') || (b.getAttribute('aria-label')||'').toLowerCase().includes('schedule'));
            if (btn) btn.click();
        })()""")
        if wait_for(
            "Boolean(document.querySelector('input[data-testid=\"date-picker-input\"]'))",
            max_sec=8
        ):
            clock_opened = True
            break
        time.sleep(2)
    if not clock_opened:
        print("  ❌ Schedule date-picker never appeared", flush=True)
        return False
    time.sleep(1)

    # ── 5. Set date via React native setter ───────────────────────────────────
    print(f"  [5/6] Setting date → {date_input}...", flush=True)
    set_res = evaluate(f"""(() => {{
        const input = document.querySelector('input[data-testid="date-picker-input"]');
        if (!input) return 'no_input';
        const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        nativeSetter.call(input, '{date_input}');
        input.dispatchEvent(new Event('input',  {{ bubbles: true }}));
        input.dispatchEvent(new Event('change', {{ bubbles: true }}));
        input.dispatchEvent(new Event('blur',   {{ bubbles: true }}));
        return input.value;
    }})()""")
    set_val = val(set_res)
    print(f"      ✓ Input value: {set_val}", flush=True)
    if set_val in (None, "no_input", ""):
        print("  ❌ date-picker-input not found", flush=True)
        return False
    time.sleep(1)

    # ── 5b. Set time (Clock) ──────────────────────────────────────────────────
    time_res = evaluate(f"""(() => {{
        const input = document.querySelector('input[data-testid="time-picker-input"]');
        if (!input) return 'no_time_input';
        const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        nativeSetter.call(input, '{post_time}');
        input.dispatchEvent(new Event('input',  {{ bubbles: true }}));
        input.dispatchEvent(new Event('change', {{ bubbles: true }}));
        input.dispatchEvent(new Event('blur',   {{ bubbles: true }}));
        return input.value;
    }})()""")
    print(f"      ✓ Time input: {val(time_res)}", flush=True)
    time.sleep(1)

    # ── 6. Confirm → Schedule ─────────────────────────────────────────────────
    print("  [6/6] Confirming & scheduling...", flush=True)

    # Click Confirm button
    evaluate("""(() => {
        const btn = Array.from(document.querySelectorAll('button'))
            .find(b => (b.innerText||'').trim() === 'Confirm' && b.offsetParent !== null);
        if (btn) btn.click();
    })()""")
    time.sleep(2)

    # Wait for Schedule button
    if not wait_for(
        "Boolean(Array.from(document.querySelectorAll('button')).find(b => (b.innerText||'').trim() === 'Schedule' && b.offsetParent !== null))",
        max_sec=10
    ):
        print("  ❌ Schedule button never appeared after Confirm", flush=True)
        return False

    # Click Schedule via JS + MouseEvent
    evaluate("""(() => {
        const btn = Array.from(document.querySelectorAll('button'))
            .find(b => (b.innerText||'').trim() === 'Schedule' && b.offsetParent !== null);
        if (btn) {
            btn.focus();
            btn.dispatchEvent(new MouseEvent('mousedown', {bubbles: true, cancelable: true, view: window}));
            btn.dispatchEvent(new MouseEvent('mouseup', {bubbles: true, cancelable: true, view: window}));
            btn.click();
        }
    })()""")
    print("      ✓ Schedule button clicked!", flush=True)
    time.sleep(4)

    print(f"  🎉 SUCCESS — Day {day_num} posted for {date_label} at {post_time}!", flush=True)
    return True

# ──────────────────────────────────────────────────────────────────────────────
# STEP 3 — VERIFY FINAL QUEUE
# ──────────────────────────────────────────────────────────────────────────────
def verify_queue():
    """Re-reads the scheduled list and prints a verification table."""
    print("\n\n🔍 FINAL VERIFICATION — Re-reading LinkedIn scheduled queue...", flush=True)
    scheduled_dates, lines = fetch_scheduled_queue()

    print(f"\n{'='*65}", flush=True)
    print("  📋 FINAL SCHEDULE STATUS", flush=True)
    print(f"{'='*65}", flush=True)
    print(f"  {'Day':<5} {'Target Date':<14} {'Status'}", flush=True)
    print(f"  {'-'*5} {'-'*14} {'-'*20}", flush=True)

    all_ok = True
    for post in CAMPAIGN:
        short = date_input_to_short(post["date_input"])
        found = any(short.lower() in s.lower() for s in scheduled_dates)
        status = "✅ SCHEDULED" if found else "❌ MISSING"
        if not found:
            all_ok = False
        print(f"  {post['day']:<5} {post['date_label']:<14} {status}", flush=True)

    print(f"{'='*65}", flush=True)
    if all_ok:
        print("  🏁 All 10 posts are confirmed scheduled!", flush=True)
    else:
        print("  ⚠  Some posts are still missing. Re-run the script.", flush=True)
    print(f"{'='*65}", flush=True)
    return all_ok

# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────
def main():
    print(f"\n{'='*65}", flush=True)
    print("  🚀 LINKEDIN SMART SCHEDULER — AUTO-DETECT & POST", flush=True)
    print(f"{'='*65}", flush=True)

    # 1. Read what's already scheduled
    scheduled_dates, _ = fetch_scheduled_queue()

    # 2. Schedule only what's missing
    skipped = 0
    posted  = 0
    failed  = 0

    for post in CAMPAIGN:
        short = date_input_to_short(post["date_input"])
        already = any(short.lower() in s.lower() for s in scheduled_dates)

        if already:
            print(f"\n  ⏭  Day {post['day']:>2} ({post['date_label']}) — already scheduled, skipping.", flush=True)
            skipped += 1
            continue

        print(f"\n  📤 Day {post['day']:>2} ({post['date_label']}) — NOT in queue, scheduling now...", flush=True)
        try:
            ok = schedule_post(post)
            if ok:
                posted += 1
                scheduled_dates.add(short)   # update local cache
            else:
                failed += 1
            time.sleep(3)
        except Exception as exc:
            print(f"  ❌ Exception on Day {post['day']}: {exc}", flush=True)
            failed += 1
            time.sleep(3)

    # 3. Summary
    print(f"\n{'='*65}", flush=True)
    print(f"  📊 RUN SUMMARY", flush=True)
    print(f"  Skipped (already scheduled) : {skipped}", flush=True)
    print(f"  Newly posted                : {posted}", flush=True)
    print(f"  Failed                      : {failed}", flush=True)
    print(f"{'='*65}", flush=True)

    # 4. Final verification
    verify_queue()


if __name__ == "__main__":
    main()
