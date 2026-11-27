#!/usr/bin/env python3
"""
validate_submission.py - checks the shape of week-11/submission.yml. DO NOT EDIT.

    python tests/validate_submission.py                # from inside week-11/
    python tests/validate_submission.py --json         # machine-readable, for the grading pipeline
    python tests/validate_submission.py --file path/to/submission.yml

It checks SHAPE, never QUALITY. A green run means the file can be read and graded, not that
the work is good. It runs tests/check_feature.py itself, so the numbers you declare are compared
with a real run, and the number of checks is never typed in by hand.

Verdicts, same vocabulary as check_feature.py:
    PASS   the field is present and well-formed
    FAIL   the field is present but wrong
    ERROR  the field is absent, or the checker could not be run to compare with

Exit codes: 0 = no FAIL and no ERROR - 1 = at least one FAIL or ERROR - 2 = file missing or
unparseable - 3 = wrong working directory.

Standard library only. No pip install, no YAML package: this file understands the restricted
subset of YAML that submission.yml uses, and refuses anything else with a line number.
"""

import argparse
import json
import os
import re
import subprocess
import sys

CHECKER = os.path.join("tests", "check_feature.py")

STUDENT_ID = re.compile(r"^\d{2}[A-Za-z]\d{6}$")
GITHUB_LOGIN = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9]|-(?=[A-Za-z0-9])){0,38}$")
SHORT_SHA = re.compile(r"^[0-9a-fA-F]{7,40}$")
CHECK_ID = re.compile(r"^(?:[BSE][12]|X[1-6]|R[1-3]|L(?:[1-9]|1[0-2]))$")
NAMES_SOMETHING = re.compile(r"\bV\d{1,2}\b|\bE[1-9]\b|\bF[1-5]\b|\bAC\s?-?[1-6]\b|\b(?:invalid_time|past_time|too_long|room_blocked|overlap)\b|\b(?:AGENTS|README)\.md\b|\b[\w/.-]+\.(?:[cm]?[jt]sx?|json|md|ya?ml)\b", re.I)
PLACEHOLDER = re.compile(r"(^<.*>$)|(\bTODO\b)|(\bFIXME\b)|(\byour name\b)|(^\.\.\.$)", re.I)

BARE_TOOL_NAMES = {
    "chatgpt", "gpt", "claude", "gemini", "copilot", "github copilot", "bolt", "bolt.new",
    "deepseek", "grok", "mistral", "llama", "qwen", "perplexity", "cursor", "lovable", "v0",
}
NOT_DISPLAYED = ("not displayed", "not-displayed")
HONESTY = ("changes_reviewed_by_me", "no_key_in_browser", "review_was_read_only", "outputs_unedited",
           "ai_usage_disclosed")
ENVIRONMENTS = ("bolt", "claude-code", "cursor", "copilot", "chat", "other")
STARTS = ("week-10", "week-08")
LANGUAGES = ("ts", "js")
ADAPTERS = ("mock", "mock-and-server")

TITLES = {
    "D1": "schema and week",
    "D2": "student.name",
    "D3": "student.student_id",
    "D4": "student.github",
    "D5": "assistant.tool",
    "D6": "assistant.model is an exact model name or not displayed",
    "D7": "environment, reviewer, project and feature",
    "D8": "checker numbers add up",
    "D9": "checker numbers match a run made now",
    "D10": "checker.commit",
    "D11": "known_fails lists exactly what still fails",
    "D12": "counts match the files and lab-report.md",
    "D13": "decision matches lab-report.md",
    "D14": "review_findings: three, each naming what it is about",
    "D15": "honesty block answered",
}


# --------------------------------------------------------------------------- parsing


class ParseError(Exception):
    pass


def strip_comment(line):
    quote = None
    for i, ch in enumerate(line):
        if quote:
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == "#" and (i == 0 or line[i - 1] in " \t"):
            return line[:i]
    return line


def scalar(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        return [scalar(part) for part in inner.split(",") if part.strip()] if inner else []
    return value


def parse(text):
    """Parse the subset submission.yml uses, and nothing else:

        key: value            at column 0
        key:                  at column 0, followed by two-space-indented lines that are
          subkey: value       either all `subkey: value`
          - item              or all `- item`
        key: [a, b]  /  []    a one-line list, at either level

    Comments start with # . Tabs are refused.
    """
    doc, current = {}, None
    for number, raw in enumerate(text.splitlines(), 1):
        if "\t" in raw[:len(raw) - len(raw.lstrip())]:
            raise ParseError("line %d: indented with a tab - use two spaces" % number)
        line = strip_comment(raw).rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        body = line.strip()
        if indent == 0:
            key, sep, value = body.partition(":")
            if not sep or not re.match(r"^[A-Za-z_][\w-]*$", key.strip()):
                raise ParseError("line %d: expected `key: value`, got %r" % (number, body[:40]))
            key = key.strip()
            if value.strip():
                doc[key], current = scalar(value), None
            else:
                doc[key], current = None, key
        elif indent == 2:
            if current is None:
                raise ParseError("line %d: indented line with no `key:` above it" % number)
            if body.startswith("-"):
                if doc[current] is None:
                    doc[current] = []
                if not isinstance(doc[current], list):
                    raise ParseError("line %d: a `- item` inside a block of `key: value` lines" % number)
                item = body[1:].strip()
                if item:
                    doc[current].append(scalar(item))
            else:
                key, sep, value = body.partition(":")
                if not sep:
                    raise ParseError("line %d: expected `key: value`, got %r" % (number, body[:40]))
                if doc[current] is None:
                    doc[current] = {}
                if not isinstance(doc[current], dict):
                    raise ParseError("line %d: a `key: value` inside a list" % number)
                doc[current][key.strip()] = scalar(value)
        else:
            raise ParseError("line %d: indent must be 0 or 2 spaces, found %d" % (number, indent))
    return doc


def get(doc, dotted):
    """Value at `a.b`, or KeyError (the class, as a marker) when the key is not there at all."""
    node = doc
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            return KeyError
        node = node[part]
    return node


def empty(value):
    return value is None or value is KeyError or (isinstance(value, str) and (
        not value.strip() or bool(PLACEHOLDER.search(value.strip()))))


def natural(check_id):
    """F2 before F10."""
    return (check_id[:1], int(check_id[1:]) if check_id[1:].isdigit() else 0)


def as_int(value):
    return int(value) if isinstance(value, str) and re.match(r"^\d+$", value.strip()) else None


# --------------------------------------------------------------------------- validation


class Report:
    def __init__(self):
        self.rows = []

    def add(self, cid, verdict, message):
        self.rows.append({"id": cid, "title": TITLES[cid], "verdict": verdict, "message": message})

    def counts(self):
        return {v: sum(1 for r in self.rows if r["verdict"] == v) for v in ("PASS", "FAIL", "ERROR")}

    def clean(self):
        c = self.counts()
        return c["FAIL"] == 0 and c["ERROR"] == 0


def text_field(rep, cid, doc, key, problem=None):
    value = get(doc, key)
    if value is KeyError:
        rep.add(cid, "ERROR", "%s: the key is missing" % key)
    elif empty(value) or not isinstance(value, str):
        rep.add(cid, "FAIL", "%s is empty" % key)
    else:
        why = problem(value.strip()) if problem else None
        rep.add(cid, "FAIL" if why else "PASS", why or "%s: %s" % (key, value.strip()))


def run_checker(folder):
    """Run the shipped checker over this folder and return its --json result, or None."""
    if not os.path.exists(os.path.join(folder, CHECKER)):
        return None
    try:
        proc = subprocess.run([sys.executable, CHECKER, "--json"], cwd=folder,
                              capture_output=True, text=True, timeout=80)
        return json.loads(proc.stdout)
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return None


def validate(doc, folder):
    rep = Report()
    run = run_checker(folder)
    now = run.get("counts") if run else None
    measured = (run or {}).get("measured") or {}

    # D1
    schema, week = get(doc, "schema"), get(doc, "week")
    ok = str(schema) == "1" and str(week) == "11"
    rep.add("D1", "PASS" if ok else "FAIL",
            "schema 1, week 11" if ok else "schema must be 1 and week must be \"11\" (got %r, %r)"
            % (None if schema is KeyError else schema, None if week is KeyError else week))

    # D2-D5
    text_field(rep, "D2", doc, "student.name")
    text_field(rep, "D3", doc, "student.student_id",
               lambda v: None if STUDENT_ID.match(v) else "%r is not a KBTU student ID (shape: 00X000000)" % v)
    text_field(rep, "D4", doc, "student.github",
               lambda v: None if GITHUB_LOGIN.match(v) else "give the GitHub username only, not a URL")
    text_field(rep, "D5", doc, "assistant.tool")

    # D6
    text_field(rep, "D6", doc, "assistant.model",
               lambda v: None if v.lower() in NOT_DISPLAYED else (
                   "%r is a tool name, not a model - give the exact model with its version, or: not displayed" % v
                   if v.lower() in BARE_TOOL_NAMES or not re.search(r"\d", v) else None))

    # D7
    probs = []
    env = get(doc, "assistant.environment")
    if env not in ENVIRONMENTS:
        probs.append("assistant.environment must be one of: " + " | ".join(ENVIRONMENTS))
    rtool, rmodel = get(doc, "reviewer.tool"), get(doc, "reviewer.model")
    if empty(rtool) or rtool is KeyError:
        probs.append("reviewer.tool is empty")
    if empty(rmodel) or rmodel is KeyError:
        probs.append("reviewer.model is empty")
    elif str(rmodel).strip().lower() not in NOT_DISPLAYED and (
            str(rmodel).strip().lower() in BARE_TOOL_NAMES or not re.search(r"\d", str(rmodel))):
        probs.append("reviewer.model %r is a tool name - give the exact model, or: not displayed" % rmodel)
    if get(doc, "reviewer.same_model_as_builder") not in ("yes", "no"):
        probs.append("reviewer.same_model_as_builder must be yes or no")
    start = get(doc, "project.starting_point")
    if start not in STARTS:
        probs.append("project.starting_point must be week-10 or week-08")
    base = get(doc, "project.baseline_commit")
    if empty(base) or base is KeyError or not SHORT_SHA.match(str(base)):
        probs.append("project.baseline_commit must be the checkpoint hash from Part 0")
    lang = get(doc, "project.language")
    if lang not in LANGUAGES:
        probs.append("project.language must be ts or js")
    vit = get(doc, "project.vitest")
    vm = re.search(r"(\d+\.\d+(?:\.\d+)?)", vit) if isinstance(vit, str) else None
    if not vm:
        probs.append("project.vitest must be the version from the RUN line, e.g. 3.2.4")
    if get(doc, "feature.adapter") not in ADAPTERS:
        probs.append("feature.adapter must be one of: " + " | ".join(ADAPTERS))
    if as_int(get(doc, "feature.timeout_ms")) is None:
        probs.append("feature.timeout_ms must be a whole number of milliseconds")
    chosen = get(doc, "feature.prompt_chosen")
    if chosen not in ("A", "B", "C"):
        probs.append("feature.prompt_chosen must be A, B or C")
    elif measured.get("prompt_chosen") and chosen != measured["prompt_chosen"]:
        probs.append("feature.prompt_chosen says %s, lab-report.md 5.4 says %s" % (chosen, measured["prompt_chosen"]))
    rep.add("D7", "FAIL" if probs else "PASS",
            "; ".join(probs) if probs else "%s, %s, %s, Vitest %s, %s adapter" % (
                env, start, lang, vm.group(1), get(doc, "feature.adapter")))

    # D8-D9
    nums = {k: as_int(get(doc, "checker." + k)) for k in ("pass", "fail", "error")}
    if now is None:
        rep.add("D8", "ERROR", "tests/check_feature.py could not be run - is it next to this file, unedited?")
        rep.add("D9", "ERROR", "no checker run to compare with")
    elif any(v is None for v in nums.values()):
        rep.add("D8", "FAIL", "checker.pass / fail / error must all be whole numbers")
        rep.add("D9", "FAIL", "nothing to compare")
    else:
        total, said = sum(now.values()), sum(nums.values())
        rep.add("D8", "PASS" if said == total else "FAIL",
                "pass + fail + error = %d" % said
                + ("" if said == total else ", but the checker runs %d checks on your files" % total))
        same = (nums["pass"], nums["fail"], nums["error"]) == (now["PASS"], now["FAIL"], now["ERROR"])
        rep.add("D9", "PASS" if same else "FAIL",
                "declared %d/%d/%d, a run now gives %d/%d/%d" % (
                    nums["pass"], nums["fail"], nums["error"], now["PASS"], now["FAIL"], now["ERROR"])
                + ("" if same else " - run the checker again and copy its numbers"))

    # D10
    commit = get(doc, "checker.commit")
    if commit is KeyError:
        rep.add("D10", "ERROR", "checker.commit: the key is missing")
    elif empty(commit) or not SHORT_SHA.match(str(commit)):
        rep.add("D10", "FAIL", "checker.commit must be the hash from git rev-parse --short HEAD, got %r" % (commit,))
    else:
        rep.add("D10", "PASS", "checker.commit: %s" % commit)

    # D11
    known = get(doc, "checker.known_fails")
    if known is KeyError:
        rep.add("D11", "ERROR", "checker.known_fails: the key is missing - write [] if nothing fails")
    elif not isinstance(known, list):
        rep.add("D11", "FAIL", "known_fails must be a list on one line, e.g. [E1] or []")
    elif run is None:
        rep.add("D11", "ERROR", "no checker run to compare with")
    else:
        bad = [x for x in known if not CHECK_ID.match(str(x))]
        failing = sorted((r["id"] for r in run.get("rows", []) if r["verdict"] != "PASS"), key=natural)
        listed = sorted(set(str(x) for x in known), key=natural)
        if bad:
            rep.add("D11", "FAIL", "known_fails holds things that are not check IDs: %s" % bad)
        elif listed != failing:
            rep.add("D11", "FAIL", "known_fails lists %s, the checker fails %s" % (listed or "[]", failing or "[]"))
        else:
            rep.add("D11", "PASS", "known_fails matches the checker: %s" % (listed or "[]"))

    # D12
    probs = []
    base = measured.get("baseline_run") or {}
    final = measured.get("final_run") or {}
    pairs = (("tests_baseline", base.get("total") if base else None),
             ("tests_final", final.get("total") if final else None),
             ("cases_run", measured.get("cases_run")),
             ("findings_verified", measured.get("findings_verified")),
             ("findings_confirmed", measured.get("findings_confirmed")))
    for key, found in pairs:
        value = as_int(get(doc, "counts." + key))
        if value is None:
            probs.append("counts.%s must be a whole number" % key)
        elif found is not None and found != value:
            probs.append("counts.%s says %d, your files say %d" % (key, value, found))
    rep.add("D12", "FAIL" if probs else "PASS", "; ".join(probs) if probs else "counts filled and match")

    # D13
    probs = []
    value, found = get(doc, "decision.fixed"), measured.get("fixed")
    if not isinstance(value, list) or len(value) != 2:
        probs.append("decision.fixed must be a list of two finding IDs, e.g. [V1, V2]")
    elif found and [str(v) for v in value] != list(found):
        probs.append("decision.fixed says %s, lab-report.md 8.1-8.2 says %s" % ([str(v) for v in value], list(found)))
    ready = get(doc, "decision.demo_ready")
    if ready not in ("yes", "no"):
        probs.append("decision.demo_ready must be yes or no")
    elif measured.get("demo_ready") and ready != measured["demo_ready"]:
        probs.append("decision.demo_ready says %s, lab-report.md 8.4 says %s" % (ready, measured["demo_ready"]))
    rep.add("D13", "FAIL" if probs else "PASS", "; ".join(probs) if probs
            else "fixed %s, demo ready: %s" % (", ".join(str(v) for v in value), ready))

    # D14
    findings = get(doc, "review_findings")
    findings = [str(f) for f in findings if str(f).strip()] if isinstance(findings, list) else []
    weak = [f for f in findings if len(f) < 25 or not NAMES_SOMETHING.search(f)]
    ok = len(findings) >= 3 and not weak
    rep.add("D14", "PASS" if ok else "FAIL",
            "%d review findings" % len(findings) if ok
            else "review_findings needs 3 or more lines, each naming a finding ID (V1), a test case (E1-E9), "
                 "a criterion (F1-F5, AC1-AC6), a reason code or a file (found %d, %d too thin)" % (len(findings), len(weak)))

    # D15
    missing = [k for k in HONESTY if get(doc, "honesty." + k) not in ("yes", "no")]
    rep.add("D15", "FAIL" if missing else "PASS",
            "must be yes or no: " + ", ".join(missing) if missing else "honesty block answered")
    return rep


# --------------------------------------------------------------------------- main


def print_human(rep, path):
    print("Week 11 submission.yml - shape only, never quality   (%s)\n" % path)
    width = max(len(r["title"]) for r in rep.rows)
    for r in rep.rows:
        print(("%-6s %-4s %-*s  %s" % (r["verdict"], r["id"], width, r["title"], r["message"])).rstrip())
    c = rep.counts()
    print("-" * 78)
    print("SUMMARY pass=%d fail=%d error=%d   (%d checks)" % (c["PASS"], c["FAIL"], c["ERROR"], len(rep.rows)))


def main():
    parser = argparse.ArgumentParser(description="Validate week-11/submission.yml")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--file", default="submission.yml")
    args = parser.parse_args()

    if args.file == "submission.yml" and not os.path.exists("submission.yml") and not os.path.isdir("tests"):
        msg = "run this from inside your week-11/ folder:  cd week-11 && python tests/validate_submission.py"
        print(json.dumps({"ok": False, "error": msg}) if args.json else "ERROR: " + msg)
        return 3
    if not os.path.exists(args.file):
        msg = "%s not found - copy it from the week-11 folder you were given" % args.file
        print(json.dumps({"ok": False, "error": msg}) if args.json else "ERROR: " + msg)
        return 2
    try:
        doc = parse(open(args.file, encoding="utf-8").read())
    except ParseError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}) if args.json else "ERROR: %s, %s" % (args.file, exc))
        return 2

    folder = os.path.dirname(os.path.abspath(args.file))
    rep = validate(doc, folder)

    def val(key):
        value = get(doc, key)
        return None if value is KeyError else value

    if args.json:
        print(json.dumps({
            "ok": rep.clean(),
            "counts": rep.counts(),
            "total": len(rep.rows),
            "rows": rep.rows,
            "declared": {
                "student_id": val("student.student_id"),
                "github": val("student.github"),
                "tool": val("assistant.tool"),
                "model": val("assistant.model"),
                "environment": val("assistant.environment"),
                "project": val("project"),
                "reviewer": val("reviewer"),
                "feature": val("feature"),
                "decision": val("decision"),
                "commit": val("checker.commit"),
                "checker": {k: as_int(val("checker." + k)) for k in ("pass", "fail", "error")},
                "known_fails": val("checker.known_fails"),
                "counts": val("counts"),
                                "findings": val("review_findings"),
            },
        }, ensure_ascii=False, indent=2))
    else:
        print_human(rep, args.file)
    return 0 if rep.clean() else 1


if __name__ == "__main__":
    sys.exit(main())
