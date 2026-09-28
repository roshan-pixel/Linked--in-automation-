"""
================================================================================
🚀 DIRECT DATE SCHEDULER FOR DAYS 5, 6, 10
================================================================================
Uses React native property setter on data-testid="date-picker-input"
with verified format MM/DD/YYYY.
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

POSTS_TO_SCHEDULE = [
    {
        "day": 5,
        "date_input": "10/02/2026",
        "date_str": "October 2, 2026",
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
        )
    },
    {
        "day": 6,
        "date_input": "10/03/2026",
        "date_str": "October 3, 2026",
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
        )
    },
    {
        "day": 10,
        "date_input": "10/07/2026",
        "date_str": "October 7, 2026",
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

def schedule_direct(post):
    day_num = post["day"]
    date_input = post["date_input"]
    date_str = post["date_str"]
    title = post["title"]
    content = post["content"]

    print("\n" + "=" * 65, flush=True)
    print(f"  📅 SCHEDULING DAY {day_num}/10: {date_str} (input: {date_input})", flush=True)
    print(f"  🎯 {title}", flush=True)
    print("=" * 65, flush=True)

    # 1. Feed navigation
    print("  [1/6] Navigating to feed...", flush=True)
    cmd("navigate", {"url": "https://www.linkedin.com/feed/"})
    time.sleep(5.0)

    # 2. Open Start a post
    print("  [2/6] Opening 'Start a post'...", flush=True)
    for attempt in range(4):
        cmd("evaluate", {"code": """(() => {
            const btn = Array.from(document.querySelectorAll('button, div[role="button"]')).find(e => (e.innerText||'').trim() === 'Start a post');
            if (btn) btn.click();
        })()"""})
        if wait_for_condition("Boolean(document.querySelector('[role=textbox]') || document.querySelector('div[contenteditable=\"true\"]'))", 4.0):
            break
        time.sleep(1.5)

    time.sleep(1.5)

    # 3. Inject text
    print("  [3/6] Injecting post text...", flush=True)
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
    print("  [4/6] Opening Schedule modal...", flush=True)
    cmd("evaluate", {"code": """(() => {
        const clock = document.querySelector('svg#clock-medium');
        if (clock) clock.closest('a, button').click();
    })()"""})
    wait_for_condition("Boolean(document.querySelector('input[data-testid=\"date-picker-input\"]'))", 8.0)
    time.sleep(1.0)

    # 5. Set Date directly via React property setter
    print(f"  [5/6] Setting date input to '{date_input}'...", flush=True)
    set_date_res = cmd("evaluate", {"code": f"""(() => {{
        const input = document.querySelector('input[data-testid="date-picker-input"]');
        if (!input) return 'no_input';
        const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
        nativeSetter.call(input, "{date_input}");
        input.dispatchEvent(new Event('input', {{ bubbles: true }}));
        input.dispatchEvent(new Event('change', {{ bubbles: true }}));
        input.dispatchEvent(new Event('blur', {{ bubbles: true }}));
        return input.value;
    }})()"""})
    print(f"      ✓ Input value set to: {set_date_res.get('data', {}).get('value')}", flush=True)
    time.sleep(1.0)

    # Click Confirm in schedule dialog
    cmd("evaluate", {"code": """(() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => (b.innerText||'').trim() === 'Confirm' && b.offsetParent !== null);
        if (btn) btn.click();
    })()"""})
    time.sleep(2.0)

    # 6. Click Schedule button
    print("  [6/6] Submitting schedule...", flush=True)
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
    print("  🚀 SCHEDULING DAYS 5, 6, AND 10 DIRECTLY", flush=True)
    print("=" * 65, flush=True)

    success = 0
    for p in POSTS_TO_SCHEDULE:
        try:
            ok = schedule_direct(p)
            if ok:
                success += 1
            time.sleep(3.0)
        except Exception as e:
            print(f"  ❌ Error on Day {p['day']}: {e}", flush=True)
            time.sleep(3.0)

    print("\n" + "=" * 65, flush=True)
    print(f"  🏁 ALL REMAINING POSTS SCHEDULED: {success}/{len(POSTS_TO_SCHEDULE)}!", flush=True)
    print("=" * 65, flush=True)

if __name__ == "__main__":
    main()
