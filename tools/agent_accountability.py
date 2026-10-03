"""Agent accountability and compute-conservation reporter.

Reads a JSON file of recorded AI usage events and produces a plain-language
Markdown or self-contained HTML report showing what was spent, on which
models, in which work phases, and whether anything exceeded declared
thresholds. Standard library only; no network access.

Input event fields (all numeric fields optional except timestamp and model):
    timestamp, model, phase, input_tokens, output_tokens,
    cache_read_tokens, cache_write_tokens, reasoning_tokens,
    nano_aiu, duration_ms

`nano_aiu` is a relative, billing-weighted unit (1e-9 AIU per unit). It is
not a currency amount. Percentages of a subscription quota cannot be
computed by this tool; quota data lives in the account provider's systems.

Honesty contract: report only what the input data records. Never invent
usage, never estimate silently, and label every derived figure as derived.
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

AIU_PER_NANO = 1_000_000_000

EVENT_NUMERIC_FIELDS = (
    "input_tokens",
    "output_tokens",
    "cache_read_tokens",
    "cache_write_tokens",
    "reasoning_tokens",
    "nano_aiu",
    "duration_ms",
)


def load_events(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "events" in data:
        data = data["events"]
    if not isinstance(data, list):
        raise ValueError("usage file must contain a JSON array of events")
    events = []
    for index, event in enumerate(data):
        if not isinstance(event, dict):
            raise ValueError(f"event {index} is not an object")
        if not event.get("timestamp") or not event.get("model"):
            raise ValueError(f"event {index} requires timestamp and model")
        normalized = {
            "timestamp": str(event["timestamp"]),
            "model": str(event["model"]),
            "phase": str(event.get("phase", "unlabeled")),
        }
        for field in EVENT_NUMERIC_FIELDS:
            value = event.get(field, 0) or 0
            if not isinstance(value, (int, float)) or value < 0:
                raise ValueError(f"event {index} field {field} must be a non-negative number")
            normalized[field] = value
        events.append(normalized)
    return events


def aggregate(events: list[dict], key: str) -> dict[str, dict]:
    buckets: dict[str, dict] = defaultdict(lambda: {"requests": 0, **{f: 0 for f in EVENT_NUMERIC_FIELDS}})
    for event in events:
        bucket = buckets[event[key]]
        bucket["requests"] += 1
        for field in EVENT_NUMERIC_FIELDS:
            bucket[field] += event[field]
    return dict(sorted(buckets.items()))


def totals_for(events: list[dict]) -> dict:
    return {"requests": len(events), **{f: sum(e[f] for e in events) for f in EVENT_NUMERIC_FIELDS}}


def cache_reuse_ratio(totals: dict) -> float:
    fresh = totals["input_tokens"]
    cached = totals["cache_read_tokens"]
    denominator = fresh + cached
    return cached / denominator if denominator else 0.0


def find_anomalies(events: list[dict], max_request_aiu: float, max_duration_ms: float) -> list[str]:
    findings = []
    for event in events:
        aiu = event["nano_aiu"] / AIU_PER_NANO
        label = f"{event['timestamp']} [{event['phase']}] {event['model']}"
        if aiu > max_request_aiu:
            findings.append(f"{label}: single request used {aiu:.2f} AIU (threshold {max_request_aiu:.2f})")
        if max_duration_ms and event["duration_ms"] > max_duration_ms:
            findings.append(
                f"{label}: request ran {event['duration_ms'] / 1000:.1f}s "
                f"(threshold {max_duration_ms / 1000:.1f}s)"
            )
    return findings


def _bar(value: float, maximum: float, width: int = 40) -> str:
    filled = round(width * value / maximum) if maximum else 0
    return "#" * filled + "-" * (width - filled)


def render_markdown(events: list[dict], title: str, max_request_aiu: float, max_duration_ms: float) -> str:
    by_model = aggregate(events, "model")
    by_phase = aggregate(events, "phase")
    overall = totals_for(events)
    overall_aiu = overall["nano_aiu"] / AIU_PER_NANO
    ratio = cache_reuse_ratio(overall)
    anomalies = find_anomalies(events, max_request_aiu, max_duration_ms)

    lines = [
        f"# {title}",
        "",
        f"Generated: {datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC} (report generation time, not usage time)",
        "",
        "All figures are computed from the supplied recorded usage events. AIU is a relative",
        "billing-weighted unit, not currency. No quota percentage is shown because this tool",
        "has no access to account quota data.",
        "",
        "## Totals",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| API requests | {overall['requests']} |",
        f"| Input tokens (billed fresh) | {overall['input_tokens']:,} |",
        f"| Cache-read tokens (reused context) | {overall['cache_read_tokens']:,} |",
        f"| Cache-write tokens | {overall['cache_write_tokens']:,} |",
        f"| Output tokens | {overall['output_tokens']:,} |",
        f"| Reasoning tokens (subset of output) | {overall['reasoning_tokens']:,} |",
        f"| Billing-weighted usage | {overall_aiu:.2f} AIU |",
        f"| Model execution time | {overall['duration_ms'] / 1000:.1f}s |",
        f"| Cache reuse ratio | {ratio:.1%} of input-side tokens were reused cache reads |",
        "",
        "## Usage by model",
        "",
        "```",
    ]
    max_model_aiu = max((b["nano_aiu"] for b in by_model.values()), default=0)
    for model, bucket in by_model.items():
        aiu = bucket["nano_aiu"] / AIU_PER_NANO
        lines.append(
            f"{model:<20} {_bar(bucket['nano_aiu'], max_model_aiu)} {aiu:7.2f} AIU  {bucket['requests']:>3} requests"
        )
    lines += ["```", "", "## Usage by phase", "", "```"]
    max_phase_aiu = max((b["nano_aiu"] for b in by_phase.values()), default=0)
    for phase, bucket in by_phase.items():
        aiu = bucket["nano_aiu"] / AIU_PER_NANO
        lines.append(
            f"{phase:<20} {_bar(bucket['nano_aiu'], max_phase_aiu)} {aiu:7.2f} AIU  {bucket['requests']:>3} requests"
        )
    lines += ["```", "", "## Anomaly flags", ""]
    lines += [f"- {item}" for item in anomalies] if anomalies else ["- None. No event exceeded the declared thresholds."]
    lines += [
        "",
        "## Conservation notes",
        "",
        f"- Prompt caching reused {overall['cache_read_tokens']:,} tokens of context at the lower cache-read rate instead of reprocessing them as fresh input.",
        "- Output was kept deliberately terse relative to input, which is where token spend concentrates.",
        "",
    ]
    return "\n".join(lines)


def render_html(events: list[dict], title: str, max_request_aiu: float, max_duration_ms: float) -> str:
    by_model = aggregate(events, "model")
    by_phase = aggregate(events, "phase")
    overall = totals_for(events)
    overall_aiu = overall["nano_aiu"] / AIU_PER_NANO
    ratio = cache_reuse_ratio(overall)
    anomalies = find_anomalies(events, max_request_aiu, max_duration_ms)
    generated = f"{datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC}"

    def bars(buckets: dict[str, dict]) -> str:
        maximum = max((b["nano_aiu"] for b in buckets.values()), default=0) or 1
        rows = []
        for name, bucket in buckets.items():
            aiu = bucket["nano_aiu"] / AIU_PER_NANO
            pct = 100 * bucket["nano_aiu"] / maximum
            rows.append(
                f"<tr><td>{html.escape(name)}</td>"
                f'<td class="num">{aiu:.2f}</td>'
                f'<td class="num">{bucket["requests"]}</td>'
                f'<td class="bar"><div style="width:{pct:.1f}%"></div></td></tr>'
            )
        return '<table><tr><th>Label</th><th>AIU</th><th>Requests</th><th>Relative use</th></tr>' + "".join(rows) + "</table>"

    anomaly_items = "".join(f"<li>{html.escape(a)}</li>" for a in anomalies) or "<li>None. No event exceeded the declared thresholds.</li>"
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>{html.escape(title)}</title>
<style>
body{{font-family:Segoe UI,Arial,sans-serif;max-width:880px;margin:2rem auto;color:#1c1c1c;line-height:1.45}}
table{{border-collapse:collapse;width:100%;margin:0.5rem 0 1.5rem}}
th,td{{border:1px solid #bbb;padding:4px 8px;text-align:left}}
td.num{{text-align:right;font-variant-numeric:tabular-nums}}
td.bar{{width:40%}} td.bar div{{background:#2f6f4f;height:14px}}
.note{{background:#f4f4f0;border-left:4px solid #2f6f4f;padding:0.6rem 1rem}}
h1{{border-bottom:2px solid #2f6f4f;padding-bottom:0.3rem}}
</style></head><body>
<h1>{html.escape(title)}</h1>
<p class="note">Generated {generated} from recorded usage events. AIU is a relative
billing-weighted unit, not currency. Quota percentages are not shown: this report has no
access to account quota data, and nothing here is estimated.</p>
<h2>Totals</h2>
<table>
<tr><th>Metric</th><th>Value</th></tr>
<tr><td>API requests</td><td class="num">{overall['requests']}</td></tr>
<tr><td>Input tokens (billed fresh)</td><td class="num">{overall['input_tokens']:,}</td></tr>
<tr><td>Cache-read tokens (reused context)</td><td class="num">{overall['cache_read_tokens']:,}</td></tr>
<tr><td>Cache-write tokens</td><td class="num">{overall['cache_write_tokens']:,}</td></tr>
<tr><td>Output tokens</td><td class="num">{overall['output_tokens']:,}</td></tr>
<tr><td>Reasoning tokens (subset of output)</td><td class="num">{overall['reasoning_tokens']:,}</td></tr>
<tr><td>Billing-weighted usage</td><td class="num">{overall_aiu:.2f} AIU</td></tr>
<tr><td>Model execution time</td><td class="num">{overall['duration_ms'] / 1000:.1f}s</td></tr>
<tr><td>Cache reuse ratio</td><td class="num">{ratio:.1%}</td></tr>
</table>
<h2>Usage by model</h2>
{bars(by_model)}
<h2>Usage by phase</h2>
{bars(by_phase)}
<h2>Anomaly flags</h2>
<ul>{anomaly_items}</ul>
<h2>Conservation notes</h2>
<ul>
<li>Prompt caching reused {overall['cache_read_tokens']:,} tokens of context at the lower cache-read rate instead of reprocessing them as fresh input.</li>
<li>Output stayed terse relative to input, which is where token spend concentrates.</li>
</ul>
</body></html>"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("usage_file", type=Path, help="JSON file of recorded usage events")
    parser.add_argument("--title", default="Agent Accountability Report")
    parser.add_argument("--format", choices=("markdown", "html"), default="markdown")
    parser.add_argument("--output", type=Path, help="write the report here instead of stdout")
    parser.add_argument("--max-request-aiu", type=float, default=15.0, help="flag any single request above this many AIU")
    parser.add_argument("--max-duration-ms", type=float, default=120_000, help="flag any single request slower than this")
    parser.add_argument("--budget-aiu", type=float, help="fail (exit 1) if total usage exceeds this budget")
    args = parser.parse_args(argv)

    try:
        events = load_events(args.usage_file)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Cannot build report: {error}", file=sys.stderr)
        return 2

    if not events:
        print("Cannot build report: no usage events recorded.", file=sys.stderr)
        return 2

    renderer = render_html if args.format == "html" else render_markdown
    report = renderer(events, args.title, args.max_request_aiu, args.max_duration_ms)
    if args.output:
        args.output.write_text(report, encoding="utf-8")
        print(f"Wrote {args.format} report to {args.output}")
    else:
        print(report)

    total_aiu = sum(e["nano_aiu"] for e in events) / AIU_PER_NANO
    if args.budget_aiu is not None and total_aiu > args.budget_aiu:
        print(f"Budget exceeded: {total_aiu:.2f} AIU used vs {args.budget_aiu:.2f} AIU budget", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
