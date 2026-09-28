# Graph Report - Linked--in-automation-  (2026-09-28)

## Corpus Check
- 58 files · ~25,186 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 201 nodes · 219 edges · 58 communities (57 shown, 1 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8d4b9c86`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]

## God Nodes (most connected - your core abstractions)
1. `schedule_post()` - 9 edges
2. `fetch_scheduled_queue()` - 7 edges
3. `🤖 LinkedIn Smart Scheduler — Auto-Post Automation via Chrome DevTools Protocol` - 7 edges
4. `schedule_linkedin_post()` - 6 edges
5. `schedule_post()` - 6 edges
6. `api_call()` - 5 edges
7. `evaluate()` - 5 edges
8. `val()` - 5 edges
9. `wait_for()` - 5 edges
10. `verify_queue()` - 5 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities (58 total, 1 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.10
Nodes (19): 1. Prerequisites, 2. Schedule Any Custom Post, 3. Run the Automated 11-Day Campaign, 🏗️ Architecture, 👤 Author, 📅 Campaign Schedule (Sep 28 – Oct 10, 2026), code:block1 (schedule_post.py  /  linkedin_scheduler.py), code:python (nativeSetter = Object.getOwnPropertyDescriptor(HTMLInputElem) (+11 more)

### Community 1 - "Community 1"
Cohesion: 0.29
Nodes (14): cmd(), date_input_to_short(), evaluate(), fetch_scheduled_queue(), main(), ================================================================================, Extract the .data.value from a WebBridge response., Poll until js_expr is truthy or timeout. Returns True/False. (+6 more)

### Community 2 - "Community 2"
Cohesion: 0.33
Nodes (12): cmd(), evaluate(), interactive_mode(), main(), normalize_date(), normalize_time(), ================================================================================, Parses various date formats and returns MM/DD/YYYY for LinkedIn. (+4 more)

### Community 3 - "Community 3"
Cohesion: 0.26
Nodes (11): api_call(), cdp_eval(), cdp_mouse_click(), find_ref_contain(), ================================================================================, Sends JSON-RPC commands to Kimi WebBridge daemon., Evaluates JavaScript expression in Chrome DevTools Protocol context., Dispatches trusted mouse pointer events via CDP. (+3 more)

### Community 4 - "Community 4"
Cohesion: 0.57
Nodes (6): api_call(), cdp_eval(), find_ref_contain(), post_now(), ================================================================================, snapshot_tree()

### Community 5 - "Community 5"
Cohesion: 0.62
Nodes (6): cmd(), evaluate(), Quick one-off post: October 10, 2026 at 6:00 PM, schedule_post(), val(), wait_for()

### Community 6 - "Community 6"
Cohesion: 0.62
Nodes (6): cmd(), evaluate(), ================================================================================, schedule_single(), val(), wait_for()

### Community 7 - "Community 7"
Cohesion: 0.53
Nodes (5): cmd(), evaluate(), Debug: find the schedule clock button in the compose modal, val(), wait_for()

### Community 8 - "Community 8"
Cohesion: 0.60
Nodes (5): cmd(), main(), ================================================================================, schedule_single_post(), wait_for_condition()

### Community 9 - "Community 9"
Cohesion: 0.67
Nodes (5): main(), ================================================================================, run_cmd(), schedule_single_post(), wait_for_condition()

### Community 10 - "Community 10"
Cohesion: 0.60
Nodes (5): cmd(), main(), ================================================================================, schedule_direct(), wait_for_condition()

### Community 11 - "Community 11"
Cohesion: 1.00
Nodes (3): cmd(), schedule_post(), wait_for_condition()

## Knowledge Gaps
- **11 isolated node(s):** `✨ Features`, `code:block1 (schedule_post.py  /  linkedin_scheduler.py)`, `code:python (nativeSetter = Object.getOwnPropertyDescriptor(HTMLInputElem)`, `1. Prerequisites`, `code:bash (python schedule_post.py)` (+6 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `Debug: find the schedule clock button in the compose modal`, `================================================================================`, `Sends JSON-RPC commands to Kimi WebBridge daemon.` to the rest of the system?**
  _32 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.1 - nodes in this community are weakly interconnected._