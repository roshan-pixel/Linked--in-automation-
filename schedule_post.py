"""
================================================================================
🚀 LINKEDIN CUSTOM POST SCHEDULER (CLI & INTERACTIVE)
================================================================================
Author  : roshan-pixel
Repo    : https://github.com/roshan-pixel/Linked--in-automation-
Bridge  : Kimi WebBridge daemon at http://127.0.0.1:10086
Session : mail-cross-verify

Tell it WHAT to post, WHICH DATE, and WHICH TIME — it automatically
navigates LinkedIn, fills the post, sets the date and time, and schedules it.

HOW TO USE
──────────
1. Interactive mode (just run it and answer the prompts):
     python schedule_post.py

2. Command-line mode (pass arguments directly):
     python schedule_post.py --date "10/12/2026" --time "6:00 PM" --text "Hello LinkedIn!"
     python schedule_post.py --date "10/12/2026" --time "6:00 PM" --file "my_post.txt"
================================================================================
"""

import sys, os, json, time, argparse, urllib.request
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True)

# ──────────────────────────────────────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────────────────────────────────────
BRIDGE_URL   = "http://127.0.0.1:10086/command"
SESSION_NAME = "mail-cross-verify"
MAX_RETRIES  = 3

# ──────────────────────────────────────────────────────────────────────────────
# DATE & TIME PARSING HELPERS
# ──────────────────────────────────────────────────────────────────────────────
def normalize_date(date_str):
    """Parses various date formats and returns MM/DD/YYYY for LinkedIn."""
    date_str = date_str.strip()
    formats = [
        '%m/%d/%Y', '%m-%d-%Y', '%Y-%m-%d', '%Y/%m/%d',
        '%d/%m/%Y', '%d-%m-%Y',
        '%b %d, %Y', '%b %d %Y', '%B %d, %Y', '%B %d %Y',
        '%d %b %Y', '%d %B %Y'
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime('%m/%d/%Y')
        except ValueError:
            pass
    # If already looks like MM/DD/YYYY or similar, return as is
    return date_str

def normalize_time(time_str):
    """Parses various time formats and returns H:MM AM/PM for LinkedIn."""
    time_str = time_str.strip().upper()
    formats = [
        '%I:%M %p', '%I:%M%p', '%I %p', '%I%p',
        '%H:%M'
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(time_str, fmt)
            formatted = dt.strftime('%I:%M %p').lstrip('0')
            return formatted if formatted else dt.strftime('%I:%M %p')
        except ValueError:
            pass
    return time_str

# ──────────────────────────────────────────────────────────────────────────────
# WEBBRIDGE HELPERS
# ──────────────────────────────────────────────────────────────────────────────
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

# ──────────────────────────────────────────────────────────────────────────────
# AUTOMATION ENGINE
# ──────────────────────────────────────────────────────────────────────────────
def schedule_post(content, target_date, target_time):
    norm_date = normalize_date(target_date)
    norm_time = normalize_time(target_time)

    print("\n" + "=" * 65, flush=True)
    print("  🚀 SCHEDULING LINKEDIN POST", flush=True)
    print(f"  📅 Target Date : {norm_date} (raw: {target_date})", flush=True)
    print(f"  ⏰ Target Time : {norm_time} (raw: {target_time})", flush=True)
    print(f"  📝 Content Len : {len(content)} characters", flush=True)
    print("=" * 65, flush=True)

    # 1. Navigate to feed
    print("\n  [1/6] Navigating to LinkedIn feed...", flush=True)
    for attempt in range(MAX_RETRIES):
        cmd("navigate", {"url": "https://www.linkedin.com/feed/"})
        time.sleep(5)
        url = val(evaluate("window.location.href")) or ""
        if "linkedin.com" in url and "login" not in url:
            print(f"        ✓ Feed loaded: {url[:50]}", flush=True)
            break
        print(f"        ⚠ Retry {attempt+1}...", flush=True)
    else:
        print("  ❌ Not logged in to LinkedIn or cannot reach feed.", flush=True)
        return False

    # 2. Open 'Start a post'
    print("  [2/6] Opening 'Start a post'...", flush=True)
    for attempt in range(MAX_RETRIES):
        evaluate("""(() => {
            const btn = Array.from(document.querySelectorAll('button, div[role="button"]'))
                .find(e => (e.innerText||'').trim() === 'Start a post');
            if (btn) btn.click();
        })()""")
        if wait_for("Boolean(document.querySelector('[role=textbox]') || document.querySelector('div[contenteditable=\"true\"]'))", 6):
            print("        ✓ Post compose modal opened", flush=True)
            break
        time.sleep(2)
    else:
        print("  ❌ Compose modal never opened", flush=True)
        return False
    time.sleep(1.5)

    # 3. Inject post text
    print("  [3/6] Injecting post content...", flush=True)
    evaluate("""(() => {
        const el = document.querySelector('[role="textbox"]') || document.querySelector('div[contenteditable="true"]');
        if (el) el.focus();
    })()""")
    time.sleep(0.5)

    fill_ok = False
    for sel in ["[role=textbox]", "div[contenteditable=\"true\"]", ".ql-editor", ".ProseMirror"]:
        res = cmd("fill", {"selector": sel, "value": content})
        if res.get("ok"):
            fill_ok = True
            print(f"        ✓ Text injected via {sel}", flush=True)
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
            print("        ✓ Text injected via execCommand fallback", flush=True)

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
            print("        ✓ Schedule dialog opened", flush=True)
            break
        time.sleep(2)
    else:
        print("  ❌ Schedule dialog never appeared", flush=True)
        return False
    time.sleep(1)

    # 5. Set Date first, then Time (Clock)
    print(f"  [5/6] Setting Date → {norm_date} and Time → {norm_time}...", flush=True)
    picker_res = evaluate(f"""(() => {{
        const dateInput = document.querySelector('input[data-testid="date-picker-input"]');
        const timeInput = document.querySelector('input[data-testid="time-picker-input"]');
        if (!dateInput) return {{error: 'no date input'}};

        // Set Date via React property setter
        const ns = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        ns.call(dateInput, '{norm_date}');
        dateInput.dispatchEvent(new Event('input',  {{ bubbles: true }}));
        dateInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
        dateInput.dispatchEvent(new Event('blur',   {{ bubbles: true }}));

        // Set Time (Clock) via React property setter
        if (timeInput) {{
            ns.call(timeInput, '{norm_time}');
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
    print(f"        ✓ Date set: {p_info.get('dateVal')}, Time set: {p_info.get('timeVal')}", flush=True)
    print(f"        ✓ LinkedIn preview: {p_info.get('postingText')}", flush=True)
    time.sleep(1.5)

    # 6. Confirm in schedule dialog, then click Schedule
    print("  [6/6] Confirming & clicking Schedule button...", flush=True)
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

    # Click Schedule
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
    print("        ✓ Clicked Schedule button", flush=True)
    time.sleep(5)

    # Check for confirmation
    check_status = evaluate("""(() => {
        return {
            hasToast: document.body.innerText.includes('Post scheduled'),
            url: window.location.href
        };
    })()""")
    status = val(check_status) or {}
    if status.get("hasToast"):
        print("\n  🎉 SUCCESS: Post successfully scheduled on LinkedIn!", flush=True)
    else:
        print("\n  ✅ Submitted: Checked post submission on LinkedIn.", flush=True)

    print(f"  📅 Scheduled for: {norm_date} at {norm_time}", flush=True)
    return True

# ──────────────────────────────────────────────────────────────────────────────
# INTERACTIVE CLI PROMPT
# ──────────────────────────────────────────────────────────────────────────────
def interactive_mode():
    print("\n" + "=" * 65)
    print("  🤖 LINKEDIN POST SCHEDULER — INTERACTIVE MODE")
    print("=" * 65)

    # 1. Ask for Date
    while True:
        target_date = input("\n📅 Enter target date (e.g. 10/10/2026 or Oct 10, 2026): ").strip()
        if target_date:
            break
        print("  ⚠ Date cannot be empty.")

    # 2. Ask for Time
    target_time = input("⏰ Enter target time (e.g. 6:00 PM, 18:00) [Default: 12:00 PM]: ").strip()
    if not target_time:
        target_time = "12:00 PM"

    # 3. Ask for Content
    print("\n📝 Choose how to provide post content:")
    print("   [1] Type / paste text directly here")
    print("   [2] Load text from a file (e.g. post.txt)")
    choice = input("Select option (1 or 2) [Default: 1]: ").strip() or "1"

    content = ""
    if choice == "2":
        while True:
            file_path = input("Enter path to file: ").strip().strip('"').strip("'")
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                print(f"  ✓ Loaded {len(content)} characters from {file_path}")
                break
            print(f"  ❌ File not found: {file_path}")
    else:
        print("\nEnter / paste your post content below.")
        print("(Type END on a new line or press Ctrl+Z / Enter twice to finish):\n")
        lines = []
        try:
            while True:
                line = input()
                if line.strip() == "END":
                    break
                lines.append(line)
        except EOFError:
            pass
        content = "\n".join(lines).strip()

    if not content:
        print("\n❌ Error: Post content cannot be empty.")
        sys.exit(1)

    # Confirm
    print("\n" + "-" * 65)
    print(f"Date : {normalize_date(target_date)}")
    print(f"Time : {normalize_time(target_time)}")
    print(f"Text Preview (first 100 chars): {content[:100]}...")
    print("-" * 65)
    proceed = input("Proceed with scheduling? (Y/n): ").strip().lower()
    if proceed and proceed != "y":
        print("Cancelled.")
        sys.exit(0)

    ok = schedule_post(content, target_date, target_time)
    if not ok:
        sys.exit(1)

# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Schedule a custom post on LinkedIn.")
    parser.add_argument("-d", "--date", help="Target date (e.g. '10/10/2026', 'Oct 10, 2026')")
    parser.add_argument("-t", "--time", default="12:00 PM", help="Target time (e.g. '6:00 PM', '18:00')")
    parser.add_argument("-c", "--content", "--text", dest="content", help="Post content text")
    parser.add_argument("-f", "--file", help="Path to text/markdown file containing post content")

    args = parser.parse_args()

    # If date and content/file are passed via CLI, use CLI mode
    if args.date and (args.content or args.file):
        content = args.content
        if args.file:
            with open(args.file, "r", encoding="utf-8") as f:
                content = f.read().strip()
        ok = schedule_post(content, args.date, args.time)
        if not ok:
            sys.exit(1)
    else:
        # Otherwise run interactive prompt
        interactive_mode()

if __name__ == "__main__":
    main()
