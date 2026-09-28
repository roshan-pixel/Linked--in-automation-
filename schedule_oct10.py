"""
================================================================================
🚀 LINKEDIN SCHEDULE POST: OCTOBER 10, 2026 AT 6:00 PM
================================================================================
Author  : roshan-pixel
Repo    : https://github.com/roshan-pixel/Linked--in-automation-
Bridge  : Kimi WebBridge daemon at http://127.0.0.1:10086
Session : mail-cross-verify

Schedules the Day 11 Grand Finale recap post for Saturday, October 10, 2026 at 6:00 PM IST.
Uses Chrome DevTools Protocol & React native property setters on LinkedIn's date & time pickers.
================================================================================
"""

import sys, json, time, urllib.request
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True)

BRIDGE_URL   = "http://127.0.0.1:10086/command"
SESSION_NAME = "mail-cross-verify"
MAX_RETRIES  = 3

POST = {
    "day":        11,
    "date_input": "10/10/2026",
    "date_label": "Oct 10, 2026",
    "post_time":  "06:00 PM",
    "title":      "10-Day Technical Showcase Grand Finale & Complete Recap",
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
    )
}

def cmd(action, args=None):
    payload = json.dumps({"action": action, "session": SESSION_NAME, "args": args or {}}).encode()
    req = urllib.request.Request(BRIDGE_URL, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read().decode())

def val(res):
    return res.get("data", {}).get("value")

def evaluate(code):
    return cmd("evaluate", {"code": code})

def wait_for(js, max_sec=12.0, step=0.5):
    deadline = time.time() + max_sec
    while time.time() < deadline:
        if val(evaluate(js)):
            return True
        time.sleep(step)
    return False

def schedule_single(post):
    date_input = post["date_input"]
    post_time  = post["post_time"]
    date_label = post["date_label"]
    title      = post["title"]
    content    = post["content"]

    print(f"\n{'='*65}", flush=True)
    print(f"  📅 Scheduling: {date_label} at {post_time}  |  {title}", flush=True)
    print(f"{'='*65}", flush=True)

    # 1. Feed navigation
    print("  [1/6] Navigating to feed...", flush=True)
    for attempt in range(MAX_RETRIES):
        cmd("navigate", {"url": "https://www.linkedin.com/feed/"})
        time.sleep(5)
        url = val(evaluate("window.location.href")) or ""
        if "linkedin.com" in url and "login" not in url:
            print(f"      ✓ Connected to feed: {url[:50]}", flush=True)
            break
        print(f"      ⚠ Retry {attempt+1}...", flush=True)
    else:
        print("  ❌ Could not load feed (not logged in?)", flush=True)
        return False

    # 2. Open compose modal
    print("  [2/6] Opening 'Start a post'...", flush=True)
    for attempt in range(MAX_RETRIES):
        evaluate("""(() => {
            const btn = Array.from(document.querySelectorAll('button, div[role="button"]'))
                .find(e => (e.innerText||'').trim() === 'Start a post');
            if (btn) btn.click();
        })()""")
        if wait_for("Boolean(document.querySelector('[role=textbox]') || document.querySelector('div[contenteditable=\"true\"]'))", 6):
            print("      ✓ Compose modal opened", flush=True)
            break
        time.sleep(2)
    else:
        print("  ❌ Compose modal never opened", flush=True)
        return False
    time.sleep(1.5)

    # 3. Inject post text
    print("  [3/6] Injecting post text...", flush=True)
    evaluate("""(() => {
        const el = document.querySelector('[role="textbox"]') || document.querySelector('div[contenteditable="true"]');
        if (el) el.focus();
    })()""")
    time.sleep(0.5)

    fill_ok = False
    for sel in ["[role=textbox]", "div[contenteditable=true]", ".ql-editor", ".ProseMirror"]:
        res = cmd("fill", {"selector": sel, "value": content})
        if res.get("ok"):
            fill_ok = True
            print(f"      ✓ Injected via {sel}", flush=True)
            break
        time.sleep(0.5)

    if not fill_ok:
        res2 = evaluate(f"""(() => {{
            const el = document.querySelector('[role="textbox"]') || document.querySelector('div[contenteditable="true"]');
            if (!el) return false;
            el.focus();
            document.execCommand('selectAll', false, null);
            document.execCommand('insertText', false, {json.dumps(content)});
            el.dispatchEvent(new Event('input', {{ bubbles: true }}));
            return true;
        }})()""")
        if val(res2):
            fill_ok = True
            print("      ✓ Injected via execCommand fallback", flush=True)

    if not fill_ok:
        print("  ❌ Could not inject post text", flush=True)
        return False
    time.sleep(1.5)

    # 4. Open Schedule modal (click clock icon)
    print("  [4/6] Opening schedule dialog...", flush=True)
    for attempt in range(MAX_RETRIES):
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
        if wait_for("Boolean(document.querySelector('input[data-testid=\"date-picker-input\"]'))", 8):
            print("      ✓ Schedule date-picker visible", flush=True)
            break
        time.sleep(2)
    else:
        print("  ❌ Schedule dialog never appeared", flush=True)
        return False
    time.sleep(1)

    # 5. Set Date first, then Clock (Time)
    print(f"  [5/6] Setting Date → {date_input} and Time → {post_time}...", flush=True)
    picker_res = evaluate(f"""(() => {{
        const dateInput = document.querySelector('input[data-testid="date-picker-input"]');
        const timeInput = document.querySelector('input[data-testid="time-picker-input"]');
        if (!dateInput) return {{error: 'no date input'}};

        // Native property setter for React-controlled date input
        const ns = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        ns.call(dateInput, '{date_input}');
        dateInput.dispatchEvent(new Event('input',  {{ bubbles: true }}));
        dateInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
        dateInput.dispatchEvent(new Event('blur',   {{ bubbles: true }}));

        // Native property setter for React-controlled time input
        if (timeInput) {{
            ns.call(timeInput, '{post_time}');
            timeInput.dispatchEvent(new Event('input',  {{ bubbles: true }}));
            timeInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
            timeInput.dispatchEvent(new Event('blur',   {{ bubbles: true }}));
        }}

        const raw = document.body.innerText;
        const postMatch = raw.match(/Posting at [^\\n]+/);
        return {{
            dateVal: dateInput.value,
            timeVal: timeInput ? timeInput.value : null,
            postingText: postMatch ? postMatch[0] : 'none'
        }};
    }})()""")
    p_info = val(picker_res) or {}
    print(f"      ✓ Date set to: {p_info.get('dateVal')}, Time set to: {p_info.get('timeVal')}", flush=True)
    time.sleep(1.5)

    # 6. Confirm in schedule dialog
    print("  [6/6] Confirming & clicking Schedule...", flush=True)
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
    time.sleep(5)

    print(f"\n  🎉 SUCCESS — Post scheduled for {date_label} at {post_time}!", flush=True)
    return True

if __name__ == "__main__":
    ok = schedule_single(POST)
    if not ok:
        sys.exit(1)
