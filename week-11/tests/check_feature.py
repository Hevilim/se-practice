#!/usr/bin/env python3
"""
check_feature.py - the Week 11 checker. DO NOT EDIT: the grader runs its own copy over your files.

    python tests/check_feature.py          # from inside week-11/
    python tests/check_feature.py --json   # machine-readable, for the grading pipeline

What it checks (27 checks):

    B1-B2    your project in app/: a package.json and canBook; nothing that must not be committed
    X1-X6    the feature in app/src/: explain.ts, the six reason codes, a timeout and a fallback,
             no key and no provider call in the browser, the "generated" label
    S1-S2    your suites: the booking suite untouched in spirit; explain.test.ts with E1-E9 titles
    E1-E2    evidence/explain-available.png and evidence/explain-fallback.png
    R1-R3    the runs you pasted: the baseline, the run after the feature, the final run
    L1-L12   lab-report.md: setup, baseline, the feature definition, the flow, the build, the
             prompts, the tests, the review, the findings, the fixes, demo readiness, reflection

It never runs your tests, never runs your code and never talks to an assistant. It reads files.
The terminal output you paste is YOUR evidence; R3 checks that it is consistent with the suite you
committed. A clean run is the floor, not the grade.

Verdicts:
    PASS   the check found what it was looking for
    FAIL   the content is there but wrong, or not enough of it
    ERROR  it could not check: a file, a folder or a section is missing

Exit codes: 0 = no FAIL and no ERROR - 1 = at least one FAIL or ERROR - 3 = wrong directory.
Standard library only.
"""

import argparse
import json
import os
import re
import struct
import sys

APP = "app"
EVIDENCE = "evidence"
REPORT = "lab-report.md"

MAX_EXPORT_MB = 5
MIN_IMAGE_BYTES = 3000
WORDS_MIN, WORDS_MAX = 80, 150
MIN_AUTOMATED, MIN_CASES_RUN, MIN_FINDINGS, MIN_CONFIRMED = 5, 8, 3, 2

CODE_EXT = (".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".mts", ".cts", ".vue", ".svelte", ".html")
IGNORED_DIRS = (".git", ".bolt", ".vscode", ".idea", "__pycache__", "node_modules", "dist", "coverage")
MODULE_NAMES = tuple("booking" + e for e in (".ts", ".js", ".tsx", ".jsx", ".mts", ".mjs"))
EXPLAIN_NAMES = tuple("explain" + e for e in (".ts", ".js", ".tsx", ".jsx", ".mts", ".mjs"))

REASON_CODES = ("available", "invalid_time", "past_time", "too_long", "room_blocked", "overlap")
CASES = tuple("E%d" % i for i in range(1, 10))

# The deck's two prompts (Tasks 3 and 6), word for word.
BUILD_PROMPT = (
    "Act as a software engineer.",
    "Extend the existing Smart Campus checker with an optional explanation feature.",
    "Preserve all booking rules and tests.",
    "The deterministic checker must remain authoritative.",
    "First, implement a mock adapter, validate inputs and outputs, handle failures gracefully, and "
    "describe each changed file.",
    "Do not add login, a database, real personal data, or client-side API secrets.")
REVIEW_PROMPT = (
    "Act as a read-only agentic code reviewer.",
    "Inspect the proposed diff in context, repository instructions, and tests.",
    "Review correctness, security, maintainability, and performance.",
    "For each issue, provide severity, affected file, evidence, reproduction or verification method, "
    "and a minimal recommendation.",
    "Do not edit files.",
    "Clearly distinguish confirmed findings from hypotheses.")
USER_STORY = "As a student, I want a short explanation of room availability so I understand the decision."

LABELS = {"confirmed": "confirmed", "plausible": "plausible", "unverified": "plausible",
          "plausible / unverified": "plausible", "plausible/unverified": "plausible",
          "unsupported": "unsupported"}
DECISIONS = ("accept", "modify", "reject")
REVIEW_CATEGORIES = ("correctness", "security", "maintainability", "performance", "tests")
SEVERITIES = ("high", "medium", "low")
COMMANDS = ("npx vitest run", "npm run build", "npm run lint")
CONTRACT_FIELDS = ("roomLabel", "start", "end", "isAvailable", "reasonCode", "explanation")
FAILURES = ("invalid input", "times out", "model fails", "contradicts")

# What must never be in the browser (README 3.5).
SECRET_LITERALS = re.compile(r"\bsk-(?:proj-|ant-)?[A-Za-z0-9_-]{20,}|\bAIza[0-9A-Za-z_-]{30,}|\bgsk_[A-Za-z0-9]{20,}|"
                             r"\bhf_[A-Za-z0-9]{20,}|Bearer\s+[A-Za-z0-9._-]{20,}")
SECRET_ENV = re.compile(r"\bVITE_[A-Z0-9_]*(?:KEY|TOKEN|SECRET)[A-Z0-9_]*\b")
PROVIDER_SDK = re.compile(r"(?:from\s*|require\s*\(\s*|import\s*\(\s*)['\"](openai|@anthropic-ai/sdk|"
                          r"@google/generative-ai|@google/genai|groq-sdk|@mistralai/mistralai|cohere-ai)['\"]")
PROVIDER_URL = re.compile(r"api\.openai\.com|api\.anthropic\.com|generativelanguage\.googleapis\.com|api\.groq\.com|"
                          r"openrouter\.ai/api|api\.mistral\.ai|api\.cohere\.(?:ai|com)|api\.deepseek\.com|"
                          r"api-inference\.huggingface\.co")

TITLES = {
    "B1": "project in app/: package.json and canBook",
    "B2": "export is clean: no node_modules, no .env, under %d MB" % MAX_EXPORT_MB,
    "X1": "src/explain.ts: explainAvailability and a mock adapter",
    "X2": "the six reason codes come from the code",
    "X3": "explain.ts has a timeout and a fallback",
    "X4": "no API key and no VITE_ secret in src/",
    "X5": "no provider SDK and no provider URL in src/",
    "X6": "the page labels the explanation as generated (F5)",
    "S1": "booking suite imports vitest and the real canBook, nothing mocked or skipped",
    "S2": "explain.test.ts: %d+ of E1-E9 in its titles, E8 or E9 among them" % MIN_AUTOMATED,
    "E1": "screenshot: evidence/explain-available.png",
    "E2": "screenshot: evidence/explain-fallback.png",
    "R1": "report 2.2: the baseline Vitest run",
    "R2": "report 6.2: the run after the feature, more tests than the baseline",
    "R3": "report 8.3: the final run, all passing, same suite",
    "L1": "report 1: builder, reviewer, models, starting point, checkpoint, Vitest",
    "L2": "report 2.1, 2.3: baseline commands; what you located",
    "L3": "report 3.1-3.3: user story, contract, F1-F5, failure behaviour",
    "L4": "report 3.4: the flow names the checker and the adapter",
    "L5": "report 4: the implementation prompt as sent, the answer, every file decided",
    "L6": "report 5: three prompts, compared, one chosen",
    "L7": "report 6.1: %d+ of E1-E9 run, and the UI row" % MIN_CASES_RUN,
    "L8": "report 7.1-7.2: reviewer context, read-only, the prompt as sent, the answer",
    "L9": "report 7.3-7.4: %d+ findings verified, %d confirmed; your own inspection" % (MIN_FINDINGS, MIN_CONFIRMED),
    "L10": "report 8.1-8.2: two confirmed findings fixed, with why and the diff",
    "L11": "report 8.4: ready for demonstration, and what remains",
    "L12": "report 10: reflection, %d-%d words, a finding ID and a test ID" % (WORDS_MIN, WORDS_MAX),
}
ORDER = list(TITLES)

# --------------------------------------------------------------------------- small helpers


class Results:
    def __init__(self):
        self.rows = []

    def add(self, cid, verdict, message):
        self.rows.append({"id": cid, "title": TITLES[cid], "verdict": verdict, "message": message})

    def counts(self):
        return {v: sum(1 for r in self.rows if r["verdict"] == v) for v in ("PASS", "FAIL", "ERROR")}


def read(path):
    try:
        return open(path, encoding="utf-8", errors="replace").read()
    except (OSError, TypeError):
        return None


def rel(path):
    return path.replace(os.sep, "/") if path else path


def walk_files(root):
    for here, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in IGNORED_DIRS)
        for name in sorted(files):
            yield os.path.join(here, name)


def project_root(folder):
    """The project: the folder itself, or the one sub-folder a downloaded zip unpacks into."""
    if not os.path.isdir(folder):
        return None
    candidates = [folder] + sorted(os.path.join(folder, d) for d in os.listdir(folder)
                                   if os.path.isdir(os.path.join(folder, d)) and d not in IGNORED_DIRS)
    for c in candidates:
        if os.path.isfile(os.path.join(c, "package.json")):
            return c
    return None


def is_test_file(path):
    return bool(re.search(r"\.(test|spec)\.[cm]?[jt]sx?$", os.path.basename(path)))


def norm(text):
    text = (text or "").replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    text = re.sub(r"[‐-―]", "-", text)
    return re.sub(r"\s+", " ", text).strip()


def strip_js_comments(src):
    src = re.sub(r"/\*.*?\*/", " ", src, flags=re.S)
    return re.sub(r"(?m)(^|[^:'\"`\\])//.*$", r"\1", src)


def image_info(path):
    """(width, height) for a real PNG or JPEG, else None."""
    try:
        data = open(path, "rb").read()
    except OSError:
        return None
    if data[:8] == b"\x89PNG\r\n\x1a\n" and len(data) > 24:
        return struct.unpack(">II", data[16:24])
    if data[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
                i += 2
                continue
            length = struct.unpack(">H", data[i + 2:i + 4])[0]
            if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                h, w = struct.unpack(">HH", data[i + 5:i + 9])
                return (w, h)
            i += 2 + length
    return None


def find_image(stem):
    if not os.path.isdir(EVIDENCE):
        return None
    for name in sorted(os.listdir(EVIDENCE)):
        base, ext = os.path.splitext(name)
        if base.lower() == stem.lower() and ext.lower() in (".png", ".jpg", ".jpeg"):
            return os.path.join(EVIDENCE, name)
    return None


def image_problem(path):
    if path is None:
        return "missing"
    if os.path.getsize(path) < MIN_IMAGE_BYTES:
        return "%s is too small to be a screenshot" % rel(path)
    if image_info(path) is None:
        return "%s is not a real PNG or JPEG" % rel(path)
    return None


def package_json(root):
    try:
        return json.loads(read(os.path.join(root, "package.json")) or "")
    except ValueError:
        return None


def deps(pkg):
    out = {}
    for key in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        if isinstance((pkg or {}).get(key), dict):
            out.update(pkg[key])
    return out


def scripts(pkg):
    s = (pkg or {}).get("scripts")
    return s if isinstance(s, dict) else {}


# --------------------------------------------------------------------------- reading a test file

TEST_CALL = re.compile(r"\b(?:test|it)((?:\.\w+)*)\s*\(\s*(['\"`])((?:\\.|(?!\2).)*?)\2", re.S)


def tests_in(src):
    """[(title, modifiers, block)] - one per test(...) / it(...) call, in order."""
    src = strip_js_comments(src or "")
    found = list(TEST_CALL.finditer(src))
    out = []
    for i, m in enumerate(found):
        end = found[i + 1].start() if i + 1 < len(found) else len(src)
        out.append((m.group(3), m.group(1) or "", src[m.start():end]))
    return out


def vitest_summaries(text):
    """Every 'Tests  1 failed | 16 passed (17)' line in text, as dicts."""
    out = []
    for line in (text or "").splitlines():
        m = re.match(r"^\s*Tests\s+(.*\(\s*(\d+)\s*\))\s*$", line)
        if not m:
            continue
        body = m.group(1)
        get = lambda word: int((re.search(r"(\d+)\s+%s" % word, body) or [0, 0])[1])
        out.append({"failed": get("failed"), "passed": get("passed"), "skipped": get("skipped"),
                    "todo": get("todo"), "total": int(m.group(2))})
    return out


def failing_names(text):
    return [l for l in (text or "").splitlines() if re.match(r"^\s*(×|✗|FAIL\b|❯.*failed)", l)]


# --------------------------------------------------------------------------- lab-report.md parsing

PLACEHOLDER = re.compile(r"\(paste here\)|^[ABC]: \(paste here\)|\(write here[^)]*\)|^<.*>$|yes / no|A / B / C|"
                         r"^\s*V\?\s*$", re.I)


def sections(text):
    """{'1': body, '6.1': body, ...} - split on the numbered '## N.' and '### N.M' headings."""
    out, current = {}, None
    for line in text.splitlines():
        m = re.match(r"^#{2,3}\s+(\d+(?:\.\d+)?)[.\s]", line)
        if m:
            current = m.group(1)
            out[current] = []
            top = current.split(".")[0]
            if top != current:
                out.setdefault(top, [])
        elif current is not None:
            out[current].append(line)
            top = current.split(".")[0]
            if top != current:
                out[top].append(line)
    return {k: "\n".join(v) for k, v in out.items()}


def table_rows(body):
    rows, lines = [], [l.strip() for l in (body or "").splitlines()]
    for i, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(re.match(r"^:?-{2,}:?$", c) for c in cells if c) and any(cells):
            continue
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if nxt.startswith("|") and re.match(r"^\|[\s:|-]+\|?$", nxt):
            continue
        rows.append(cells)
    return rows


def clean_cell(cell):
    return re.sub(r"<!--.*?-->", "", cell or "").strip().strip("*`").strip()


def useful(cell):
    cell = clean_cell(cell)
    return bool(cell) and not PLACEHOLDER.search(cell)


def blocks(body):
    return re.findall(r"```[^\n]*\n(.*?)```", body or "", re.S)


def strip_comments(body):
    return re.sub(r"<!--.*?-->", " ", body or "", flags=re.S)


def word_count(body):
    body = strip_comments(body)
    body = re.sub(r"```.*?```", " ", body, flags=re.S)
    body = "\n".join(l for l in body.splitlines() if not l.lstrip().startswith((">", "|", "#")))
    return len(re.findall(r"[^\W_]+(?:['’-][^\W_]+)*", body))


def after_marker(body, marker="Write below this line"):
    return body.split(marker, 1)[1] if marker in (body or "") else (body or "")


def as_int(cell):
    m = re.match(r"^\s*(\d+)\s*$", clean_cell(cell))
    return int(m.group(1)) if m else None


def category_of(cell):
    low = clean_cell(cell).lower()
    for key, name in CATEGORIES:
        if key in low:
            return name
    return None


def risk_ids(text):
    return re.findall(r"\bR(\d{1,2})\b", text or "")


def is_diff(text):
    return bool(re.search(r"(?m)^\s*-(?!--)\s*\S", text or "") and re.search(r"(?m)^\s*\+(?!\+\+)\s*\S", text or ""))


def contains_prompt(sent, prompt):
    have = norm(sent)
    return [s for s in prompt if norm(s) not in have]


# --------------------------------------------------------------------------- B, S: the project


def find_module(root):
    hits = [p for p in walk_files(root) if os.path.basename(p) in MODULE_NAMES]
    hits.sort(key=lambda p: (0 if "/src/" in rel(p) + "/" else 1, len(p)))
    return hits[0] if hits else None


def find_suite(module):
    if not module:
        return None
    folder = os.path.dirname(module)
    for name in sorted(os.listdir(folder)):
        if re.match(r"^booking\.(test|spec)\.[cm]?[jt]sx?$", name):
            return os.path.join(folder, name)
    return None


def check_project(res, measured):
    root = project_root(APP)
    measured["app_root"] = rel(root)
    module = find_module(root) if root else None
    measured["module"] = rel(module)
    src = strip_js_comments(read(module) or "") if module else ""
    if not root:
        res.add("B1", "ERROR", "no package.json in app/ - bring your Week 10 app/ over (README Part 0)")
    elif not module:
        res.add("B1", "ERROR", "no booking.ts / booking.js in the project")
    elif not re.search(r"\bfunction\s+canBook\b|\bcanBook\s*=", src):
        res.add("B1", "FAIL", "%s does not define canBook" % rel(module))
    else:
        res.add("B1", "PASS", "%s, canBook" % rel(module))

    problems = []
    if os.path.isdir(APP):
        size = 0
        for here, dirs, names in os.walk(APP):
            if "node_modules" in dirs:
                problems.append("%s contains node_modules/ - delete it" % rel(here))
                dirs.remove("node_modules")
            for n in names:
                if n == ".env" or (n.startswith(".env.") and n != ".env.example"):
                    problems.append("%s/%s must not be committed" % (rel(here), n))
                try:
                    size += os.path.getsize(os.path.join(here, n))
                except OSError:
                    pass
        if size > MAX_EXPORT_MB * 1024 * 1024:
            problems.append("app/ is %.1f MB - commit source files only" % (size / 1048576.0))
    if not root:
        res.add("B2", "ERROR", "nothing to check until app/ holds the project")
    else:
        res.add("B2", "FAIL" if problems else "PASS", "; ".join(problems) if problems else "clean")
    return root, module




def check_booking_suite(res, measured, root, module):
    suite = find_suite(module)
    measured["suite"] = rel(suite)
    measured["tests_in_project"] = sum(len(tests_in(read(p) or "")) for p in walk_files(root) if is_test_file(p)) \
        if root else 0
    if suite is None:
        res.add("S1", "ERROR", "no booking.test.ts / booking.test.js beside %s" % (rel(module) or "the booking module"))
        return
    src = read(suite)
    tests = tests_in(src)
    clean = strip_js_comments(src or "")
    bad = []
    if not re.search(r"from\s*['\"]vitest['\"]", clean):
        bad.append("import { test, expect } from 'vitest'")
    if not re.search(r"import\s*\{[^}]*\bcanBook\b[^}]*\}\s*from\s*['\"]\./booking(?:\.[cm]?[jt]sx?)?['\"]", clean):
        bad.append("import { canBook } from './booking'")
    if re.search(r"\b(?:vi|jest)\.(?:mock|doMock|spyOn)\s*\(", clean):
        bad.append("no mock or spy of the booking module")
    bad += skipped(tests, clean)
    res.add("S1", "FAIL" if bad else "PASS",
            "the suite needs: " + "; ".join(bad) if bad else "%s: %d tests, real canBook" % (rel(suite), len(tests)))


def skipped(tests, clean):
    bad = []
    for m in sorted(set(m for _, m, _ in tests if m)):
        if re.search(r"\.(skip|only|todo|fails|skipIf|runIf)\b", m):
            bad.append("no test%s" % m)
    if re.search(r"\b(?:describe|suite)\.(?:skip|only|todo)\b|\bx(?:it|test|describe)\s*\(", clean):
        bad.append("no skipped or focused describe block")
    return bad


# --------------------------------------------------------------------------- X: the feature


def find_explain(root):
    hits = [p for p in walk_files(root) if os.path.basename(p) in EXPLAIN_NAMES]
    hits.sort(key=lambda p: (0 if "/src/" in rel(p) + "/" else 1, len(p)))
    return hits[0] if hits else None


def src_files(root):
    """Every code file under app/src/ (what ships to the browser), tests excluded."""
    base = os.path.join(root, "src") if root and os.path.isdir(os.path.join(root, "src")) else root
    if not base:
        return []
    return [p for p in walk_files(base) if p.endswith(CODE_EXT) and not is_test_file(p)]


def check_feature(res, measured, root, module):
    explain = find_explain(root) if root else None
    measured["explain_module"] = rel(explain)
    src = strip_js_comments(read(explain) or "") if explain else ""
    if not root:
        for cid in ("X1", "X2", "X3", "X4", "X5", "X6"):
            res.add(cid, "ERROR", "no project in app/ - bring your Week 10 app/ over (README Part 0)")
        return
    if not explain:
        res.add("X1", "ERROR", "no explain.ts / explain.js in the project (README 3.3)")
    else:
        miss = []
        if not re.search(r"\bexport\b[^\n;]*\bexplainAvailability\b|\bexport\s*\{[^}]*\bexplainAvailability\b", src):
            miss.append("an exported explainAvailability")
        if not re.search(r"\bexport\b[^\n;]*\b\w*mock\w*\b|\bexport\s*\{[^}]*\b\w*mock\w*\b", src, re.I):
            miss.append("an exported mock adapter (a name containing mock)")
        res.add("X1", "FAIL" if miss else "PASS",
                "%s needs %s" % (rel(explain), " and ".join(miss)) if miss else "%s: explainAvailability, mock adapter" % rel(explain))

    blob = "\n".join(strip_js_comments(read(p) or "") for p in ([module] if module else []) + ([explain] if explain else []))
    missing = [c for c in REASON_CODES if not re.search(r"['\"`]%s['\"`]" % c, blob)]
    if not module:
        res.add("X2", "ERROR", "no booking module to read")
    else:
        res.add("X2", "FAIL" if missing else "PASS", "not found as strings in the booking or explain module: "
                + ", ".join(missing) + " (README 3.1)" if missing else "six reason codes")

    if not explain:
        res.add("X3", "ERROR", "no explain module to read")
    else:
        miss = []
        if not re.search(r"\bsetTimeout\s*\(|\bAbortController\b|AbortSignal\.timeout", src):
            miss.append("a timeout (setTimeout, AbortController or AbortSignal.timeout)")
        if not re.search(r"fallback", src, re.I):
            miss.append("a fallback")
        res.add("X3", "FAIL" if miss else "PASS", "%s needs %s" % (rel(explain), " and ".join(miss)) if miss
                else "timeout and fallback in %s" % rel(explain))

    files = src_files(root)
    keys, envs, sdks, urls = [], [], [], []
    for p in files:
        raw = read(p) or ""
        if SECRET_LITERALS.search(raw):
            keys.append(rel(os.path.relpath(p, APP)))
        for m in SECRET_ENV.findall(raw):
            envs.append("%s in %s" % (m, rel(os.path.relpath(p, APP))))
        code = strip_js_comments(raw)
        for m in PROVIDER_SDK.findall(code):
            sdks.append("'%s' in %s" % (m, rel(os.path.relpath(p, APP))))
        if PROVIDER_URL.search(code):
            urls.append(rel(os.path.relpath(p, APP)))
    for p in walk_files(root):
        if os.path.basename(p) == ".env" and p not in keys:
            keys.append(rel(os.path.relpath(p, APP)))
    measured["browser_secrets"] = keys + envs
    measured["browser_provider_calls"] = sdks + urls
    probs = (["a key-like string in " + ", ".join(sorted(set(keys)))] if keys else []) + sorted(set(envs))
    res.add("X4", "FAIL" if probs else "PASS", "in the browser: " + "; ".join(probs) + " - keys stay on a server "
            "(README 3.5)" if probs else "no key or VITE_ secret in %d source files" % len(files))
    probs = sorted(set(sdks)) + (["a provider URL in " + ", ".join(sorted(set(urls)))] if urls else [])
    res.add("X5", "FAIL" if probs else "PASS", "the page talks to a model directly: " + "; ".join(probs) +
            " - use the mock adapter, or a server outside src/" if probs else "no provider SDK or URL in src/")

    ui = [p for p in files if re.search(r"\.(tsx|jsx|vue|svelte|html)$", p)]
    labelled = [p for p in ui if re.search(r"generated", strip_js_comments(read(p) or ""), re.I)]
    if not ui:
        res.add("X6", "ERROR", "no .tsx / .jsx page in src/")
    else:
        res.add("X6", "PASS" if labelled else "FAIL", "label in %s" % rel(os.path.relpath(labelled[0], APP)) if labelled
                else "no page file says 'generated': label the explanation so it cannot be taken for the status (F5)")


def check_feature_suite(res, measured, root):
    suites = [p for p in walk_files(root) if is_test_file(p) and re.match(r"^explain\.", os.path.basename(p))] if root else []
    if not suites:
        res.add("S2", "ERROR", "no explain.test.ts in the project (README Part 5)")
        measured["cases_automated"] = []
        return
    suite = suites[0]
    src = read(suite) or ""
    clean = strip_js_comments(src)
    tests = tests_in(src)
    ids = sorted(set(m for title, _, _ in tests for m in re.findall(r"^\s*(E[1-9])\b", title)), key=lambda c: int(c[1:]))
    measured["cases_automated"] = ids
    bad = []
    if not re.search(r"from\s*['\"]vitest['\"]", clean):
        bad.append("import from 'vitest'")
    if not re.search(r"from\s*['\"]\./explain(?:\.[cm]?[jt]sx?)?['\"]", clean):
        bad.append("an import from './explain'")
    if len(ids) < MIN_AUTOMATED:
        bad.append("%d+ test titles starting with E1-E9 (found %s)" % (MIN_AUTOMATED, ", ".join(ids) or "none"))
    if not ({"E8", "E9"} & set(ids)):
        bad.append("E8 or E9 automated, with a fake adapter that hangs or throws")
    bad += skipped(tests, clean)
    res.add("S2", "FAIL" if bad else "PASS", "%s needs: %s" % (rel(suite), "; ".join(bad)) if bad
            else "%s: %s" % (rel(suite), " ".join(ids)))


# --------------------------------------------------------------------------- L: the worksheet


def check_setup(res, sec):
    rows = [(clean_cell(r[0]).lower(), r[1]) for r in table_rows(sec.get("1", "")) if len(r) > 1]
    lacking = []
    need = (("built the feature", "the builder tool"), ("reviewed with", "the reviewer tool"),
            ("starting point", "the starting point"), ("baseline commit", "the baseline commit"),
            ("ran the tests", "where you ran the tests"), ("vitest version", "the Vitest version"))
    for key, say in need:
        if not any(key in k and useful(v) for k, v in rows):
            lacking.append(say)
    models = [v for k, v in rows if "exact model" in k]
    if len(models) < 2 or not all(useful(v) for v in models[:2]):
        lacking.append("both exact models (or not displayed)")
    start = next((clean_cell(v) for k, v in rows if "starting point" in k), "")
    commit = next((clean_cell(v) for k, v in rows if "baseline commit" in k), "")
    if start and useful(start) and not re.search(r"\bweek-(?:10|08)\b", start):
        lacking.append("a starting point of week-10 or week-08")
    if commit and useful(commit) and not re.search(r"\b[0-9a-f]{7,40}\b", commit):
        lacking.append("the baseline commit as a hash")
    res.add("L1", "FAIL" if lacking else "PASS",
            "section 1 needs: " + ", ".join(lacking) if lacking else "setup recorded")


def check_baseline(res, measured, sec):
    rows = table_rows(sec.get("2.1", ""))
    probs = []
    for cmd in COMMANDS:
        row = next((r for r in rows if r and norm(clean_cell(r[0])).startswith(cmd)), None)
        ok = row is not None and len(row) >= 3 and clean_cell(row[1]).lower() in ("yes", "no") and \
            clean_cell(row[2]).lower() in ("pass", "fail", "missing", "not run")
        if not ok:
            probs.append(cmd)
    probs = ["2.1: exists (yes/no) and result (pass/fail/missing/not run) for " + ", ".join(probs)] if probs else []
    found = {clean_cell(r[0]).lower(): r for r in table_rows(sec.get("2.3", "")) if r}
    for what in ("availability function", "ui component", "repository instructions"):
        r = next((v for k, v in found.items() if what in k), None)
        if not r or len(r) < 2 or not useful(r[1]):
            probs.append("2.3: where to find the %s" % what)
    res.add("L2", "FAIL" if probs else "PASS", "section " + "; ".join(probs) if probs
            else "three commands recorded, three things located")

    s22 = vitest_summaries(" ".join(blocks(sec.get("2.2", ""))))
    measured["baseline_run"] = s22[-1] if s22 else None
    if not s22:
        res.add("R1", "FAIL", "section 2.2 has no Vitest output - run npx vitest run before any change")
    else:
        res.add("R1", "PASS", "%(passed)d passed, %(failed)d failed (%(total)d)" % s22[-1])


def check_definition(res, sec):
    probs = []
    if norm(USER_STORY) not in norm(strip_comments(sec.get("3.1", ""))):
        probs.append("3.1: the deck's user story, exactly")
    rows = {clean_cell(r[0]).strip("`").lower(): r for r in table_rows(sec.get("3.2", "")) if r}
    thin = [f for f in CONTRACT_FIELDS if not (rows.get(f.lower()) and len(rows[f.lower()]) >= 4
                                                 and useful(rows[f.lower()][2]) and useful(rows[f.lower()][3]))]
    if thin:
        probs.append("3.2: type and validation for " + ", ".join(thin))
    s33 = strip_comments(after_marker(sec.get("3.3", "")))
    have = set(re.findall(r"\bF([1-5])\b", s33.split("| Failure", 1)[0]))
    if len(have) < 5:
        probs.append("3.3: F1-F5 written out (found %s)" % (", ".join("F" + h for h in sorted(have)) or "none"))
    fails = {clean_cell(r[0]).lower(): r for r in table_rows(s33) if r}
    lacking = [f for f in FAILURES if not any(f in k and len(r) > 1 and useful(r[1]) for k, r in fails.items())]
    if lacking:
        probs.append("3.3: what the student sees when " + ", ".join(lacking))
    res.add("L3", "FAIL" if probs else "PASS", "section " + "; ".join(probs) if probs
            else "user story, six fields, F1-F5, four failures")

    flow = " ".join(blocks(sec.get("3.4", "")))
    probs = []
    if PLACEHOLDER.search(flow) or len(re.findall(r"->|→|-->|=>", flow)) < 3:
        probs.append("three or more arrows")
    if not re.search(r"canBook|availabilityReason|checker|rule engine", flow, re.I):
        probs.append("the checker function")
    if not re.search(r"adapter", flow, re.I):
        probs.append("the adapter")
    if not re.search(r"decid", flow + strip_comments(sec.get("3.4", "")), re.I):
        probs.append("which one decides")
    res.add("L4", "FAIL" if probs else "PASS", "section 3.4: the flow needs " + ", ".join(probs) if probs
            else "checker and adapter, who decides")


def check_build(res, sec):
    b = blocks(sec.get("4.1", ""))
    probs = []
    lost = contains_prompt(" ".join(b[:1]), BUILD_PROMPT)
    if lost:
        probs.append("4.1: the deck's prompt exactly as sent (missing: \"%s\")" % lost[0][:60])
    if len(b) < 2 or len(norm(b[1]).split()) < 30 or PLACEHOLDER.search(b[1]):
        probs.append("4.1: the assistant's answer (30+ words)")
    decided = [r for r in table_rows(sec.get("4.2", "")) if len(r) >= 4 and useful(r[0]) and useful(r[1])
               and clean_cell(r[2]).lower() in DECISIONS and useful(r[3])]
    if len(decided) < 2:
        probs.append("4.2: two or more changed files with accept / modify / reject and why (found %d)" % len(decided))
    rows = {clean_cell(r[0]).lower(): r for r in table_rows(sec.get("4.3", "")) if r}
    for key, say in (("mock adapter", "the mock adapter's name"), ("timeout", "the timeout"),
                     ("real-model", "whether there is a real-model adapter")):
        r = next((v for k, v in rows.items() if key in k), None)
        if not r or len(r) < 2 or not useful(r[1]):
            probs.append("4.3: " + say)
    res.add("L5", "FAIL" if probs else "PASS", "section " + "; ".join(probs) if probs
            else "prompt as sent, answer, %d files decided" % len(decided))


def check_prompts(res, measured, sec):
    probs = []
    pb = [x for x in blocks(sec.get("5.1", "")) if not PLACEHOLDER.search(x) and len(norm(x).split()) >= 8]
    if len(pb) < 3:
        probs.append("5.1: three instructions, 8+ words each (found %d)" % len(pb))
    elif len(set(norm(x).lower() for x in pb)) < 3:
        probs.append("5.1: three different instructions")
    ans = " ".join(blocks(sec.get("5.2", "")))
    if PLACEHOLDER.search(ans) or len(norm(ans).split()) < 40:
        probs.append("5.2: the inputs and the answers (40+ words)")
    rows = {clean_cell(r[0]).upper(): r for r in table_rows(sec.get("5.3", "")) if r}
    for p in "ABC":
        r = rows.get(p)
        if not r or len(r) < 5 or as_int(r[1]) not in (1, 2, 3) or as_int(r[2]) not in (1, 2, 3) \
                or clean_cell(r[3]).lower() not in ("yes", "no") or not useful(r[4]):
            probs.append("5.3: row %s (clarity 1-3, consistency 1-3, agrees yes/no, invented)" % p)
    body = strip_comments(sec.get("5.4", ""))
    m = re.search(r"Chosen:\**\s*\**\s*([ABC])\b(?!\s*/)", body)
    measured["prompt_chosen"] = m.group(1) if m else None
    if not m:
        probs.append("5.4: one letter after **Chosen:**")
    elif word_count(body.split(m.group(0), 1)[1]) < 10:
        probs.append("5.4: why (10+ words)")
    res.add("L6", "FAIL" if probs else "PASS", "section " + "; ".join(probs[:3]) +
            (" (+%d more)" % (len(probs) - 3) if len(probs) > 3 else "") if probs
            else "three prompts compared, %s chosen" % m.group(1))


def check_cases(res, measured, sec):
    rows = {clean_cell(r[0]).upper(): r for r in table_rows(sec.get("6.1", "")) if r}
    run, thin = [], []
    for cid in CASES:
        r = rows.get(cid)
        verdict = clean_cell(r[4]).lower() if r and len(r) >= 6 else ""
        if verdict in ("pass", "fail") and all(useful(c) for c in (r[2], r[3], r[5])):
            run.append(cid)
        elif verdict == "not run" and useful(r[3] if r else ""):
            pass
        elif r is None or verdict not in ("pass", "fail", "not run"):
            thin.append(cid)
    measured["cases_run"] = len(run)
    probs = []
    if len(run) < MIN_CASES_RUN:
        probs.append("%d of E1-E9 with expected, observed, pass/fail and how; %d needed" % (len(run), MIN_CASES_RUN))
    if thin:
        probs.append("a verdict for " + ", ".join(thin))
    ui = rows.get("UI")
    if not ui or len(ui) < 6 or not all(useful(c) for c in (ui[2], ui[3], ui[5])) \
            or clean_cell(ui[4]).lower() not in ("pass", "fail"):
        probs.append("the UI row: the page never changes the decision, checked and how")
    shots = {clean_cell(r[0]).lower(): r for r in table_rows(sec.get("6.3", "")) if r}
    if sum(1 for k, r in shots.items() if "evidence/" in k and len(r) > 1 and useful(r[1])) < 2:
        probs.append("6.3: what each screenshot shows")
    res.add("L7", "FAIL" if probs else "PASS", "section 6: " + "; ".join(probs) if probs
            else "%d of 9 cases run, the UI row checked" % len(run))

    s62 = vitest_summaries(" ".join(blocks(sec.get("6.2", ""))))
    base = measured.get("baseline_run")
    measured["feature_run"] = s62[-1] if s62 else None
    if not s62:
        res.add("R2", "FAIL", "section 6.2 has no Vitest output of the suite with explain.test.ts")
    elif base and s62[-1]["total"] <= base["total"]:
        res.add("R2", "FAIL", "the run reports %d tests, the baseline %d - the feature tests are missing from it"
                % (s62[-1]["total"], base["total"]))
    else:
        res.add("R2", "PASS", "%(passed)d passed, %(failed)d failed (%(total)d)" % s62[-1])


def check_review(res, sec):
    s71 = after_marker(sec.get("7.1", ""))
    probs = []
    if word_count(s71) < 15:
        probs.append("7.1: where it ran, how it could not edit, and what it was given (15+ words)")
    elif not re.search(r"\bdiff\b", s71, re.I):
        probs.append("7.1: say whether the reviewer got the diff")
    b = blocks(sec.get("7.2", ""))
    lost = contains_prompt(b[0] if b else "", REVIEW_PROMPT)
    if lost:
        probs.append("7.2: the deck's prompt exactly as sent (missing: \"%s\")" % lost[0][:60])
    if len(b) < 2 or len(norm(b[1]).split()) < 50 or PLACEHOLDER.search(b[1]):
        probs.append("7.2: the reviewer's answer (50+ words)")
    res.add("L8", "FAIL" if probs else "PASS", "section " + "; ".join(probs) if probs
            else "context, read-only, prompt as sent, answer")


def check_findings(res, measured, sec):
    findings, probs = {}, []
    for r in table_rows(sec.get("7.3", "")):
        if not r or not re.match(r"^V\d{1,2}$", clean_cell(r[0])) or len(r) < 8 or not any(useful(c) for c in r[1:]):
            continue
        fid = clean_cell(r[0])
        miss = [n for n, c in zip(("finding", "category", "severity", "file", "how verified", "label", "found by"), r[1:8])
                if not useful(c)]
        label = LABELS.get(clean_cell(r[6]).lower())
        findings[fid] = label
        if miss:
            probs.append("%s: empty %s" % (fid, ", ".join(miss)))
            continue
        if clean_cell(r[2]).lower() not in REVIEW_CATEGORIES:
            probs.append("%s: category is one of %s" % (fid, "/".join(REVIEW_CATEGORIES)))
        if clean_cell(r[3]).lower() not in SEVERITIES:
            probs.append("%s: severity is high/medium/low" % fid)
        if not label:
            probs.append("%s: label is confirmed, plausible or unsupported" % fid)
        if clean_cell(r[7]).lower() not in ("reviewer", "me", "both"):
            probs.append("%s: found by reviewer, me or both" % fid)
        if len(re.findall(r"[^\W_]+", clean_cell(r[5]))) < 4:
            probs.append("%s: how you verified it (4+ words)" % fid)
    confirmed = sorted(k for k, v in findings.items() if v == "confirmed")
    measured["findings_verified"] = len(findings)
    measured["findings_confirmed"] = len(confirmed)
    if len(findings) < MIN_FINDINGS:
        probs.insert(0, "%d findings, %d needed" % (len(findings), MIN_FINDINGS))
    if len(confirmed) < MIN_CONFIRMED:
        probs.append("%d confirmed, %d needed" % (len(confirmed), MIN_CONFIRMED))
    if word_count(after_marker(sec.get("7.4", ""))) < 20:
        probs.append("7.4: your own inspection and the linter (20+ words)")
    res.add("L9", "FAIL" if probs else "PASS", "section 7: " + "; ".join(probs[:3]) +
            (" (+%d more)" % (len(probs) - 3) if len(probs) > 3 else "") if probs
            else "%d findings, %d confirmed, own inspection" % (len(findings), len(confirmed)))
    return findings


def check_fixes(res, measured, sec, findings):
    ids, probs = [], []
    for key in ("8.1", "8.2"):
        body = strip_comments(sec.get(key, ""))
        m = re.search(r"Finding:\**\s*\**\s*(V\d{1,2})\b", body)
        fid = m.group(1) if m else None
        ids.append(fid)
        if not fid:
            probs.append("%s: the finding ID (**Finding:** V1)" % key)
            continue
        if fid not in findings:
            probs.append("%s: %s is not in 7.3" % (key, fid))
        elif findings[fid] != "confirmed":
            probs.append("%s: %s is not confirmed" % (key, fid))
        why = body.split("necessary:", 1)[1].split("What I rejected", 1)[0] if "necessary:" in body else ""
        if word_count(why) < 8:
            probs.append("%s: why it is necessary (8+ words)" % key)
        rejected = body.split("and why:", 1)[1].split("The diff", 1)[0] if "and why:" in body else ""
        if word_count(rejected) < 3:
            probs.append("%s: what you rejected (or 'nothing', with why)" % key)
        if not is_diff(" \n".join(blocks(body))):
            probs.append("%s: the diff" % key)
    if ids[0] and ids[0] == ids[1]:
        probs.append("two different findings")
    measured["fixed"] = [i for i in ids if i]
    res.add("L10", "FAIL" if probs else "PASS", "section 8: " + "; ".join(probs[:3]) +
            (" (+%d more)" % (len(probs) - 3) if len(probs) > 3 else "") if probs
            else "%s and %s fixed" % tuple(ids))

    s83 = vitest_summaries(" ".join(blocks(sec.get("8.3", ""))))
    if not s83:
        res.add("R3", "FAIL", "section 8.3 has no Vitest output of the final suite")
    else:
        f = s83[-1]
        measured["final_run"] = f
        probs = []
        if f["failed"]:
            probs.append("%d failed" % f["failed"])
        have = measured.get("tests_in_project")
        if have and f["total"] != have:
            probs.append("the output reports %d tests, the test files in app/ hold %d - paste the run of the "
                         "suite you committed" % (f["total"], have))
        base = measured.get("baseline_run")
        if base and f["total"] <= base["total"]:
            probs.append("%d tests, no more than the baseline's %d - every old test stays and the feature adds its own"
                         % (f["total"], base["total"]))
        res.add("R3", "FAIL" if probs else "PASS", "; ".join(probs) if probs else "%(passed)d passed (%(total)d)" % f)

    body = strip_comments(sec.get("8.4", ""))
    m = re.search(r"Ready:\**\s*\**\s*(yes|no)\b(?!\s*/)", body, re.I)
    measured["demo_ready"] = m.group(1).lower() if m else None
    rest = after_marker(sec.get("8.4", ""))
    probs = []
    if not m:
        probs.append("yes or no after **Ready:**")
    if word_count(rest) < 8:
        probs.append("what remains unresolved (8+ words; 'nothing' needs its reason)")
    res.add("L11", "FAIL" if probs else "PASS", "section 8.4 needs " + "; ".join(probs) if probs
            else "ready: %s, what remains named" % m.group(1).lower())


def check_reflection(res, measured, sec):
    text = after_marker(sec.get("10", ""), "Write your reflection below this line")
    words = word_count(text)
    measured["reflection_words"] = words
    clean = strip_comments(text)
    probs = []
    if not WORDS_MIN <= words <= WORDS_MAX:
        probs.append("%d words, the task asks for %d-%d" % (words, WORDS_MIN, WORDS_MAX))
    if not re.search(r"\bV\d{1,2}\b", clean):
        probs.append("a finding ID (V1...)")
    if not re.search(r"\bE[1-9]\b", clean):
        probs.append("a test ID (E1-E9)")
    res.add("L12", "FAIL" if probs else "PASS", "section 10: " + "; ".join(probs) if probs else "%d words" % words)


# --------------------------------------------------------------------------- main


def run():
    res, measured = Results(), {}
    root, module = check_project(res, measured)
    check_feature(res, measured, root, module)
    if root:
        check_booking_suite(res, measured, root, module)
        check_feature_suite(res, measured, root)
    else:
        res.add("S1", "ERROR", "no project in app/")
        res.add("S2", "ERROR", "no project in app/")
    for cid, stem in (("E1", "explain-available"), ("E2", "explain-fallback")):
        p = find_image(stem)
        why = image_problem(p)
        res.add(cid, "PASS" if not why else ("FAIL" if p else "ERROR"),
                rel(p) if not why else (why if p else "evidence/%s.png not found - the screenshots of Part 5" % stem))
    text = read(REPORT)
    if text is None:
        for cid in ORDER:
            if cid[0] in "RL":
                res.add(cid, "ERROR", "lab-report.md not found")
    else:
        sec = sections(text)
        check_setup(res, sec)
        check_baseline(res, measured, sec)
        check_definition(res, sec)
        check_build(res, sec)
        check_prompts(res, measured, sec)
        check_cases(res, measured, sec)
        check_review(res, sec)
        findings = check_findings(res, measured, sec)
        check_fixes(res, measured, sec, findings)
        check_reflection(res, measured, sec)
    res.rows = sorted(res.rows, key=lambda r: ORDER.index(r["id"]))
    return res, measured


def print_human(res, measured):
    counts = res.counts()
    print("Week 11 - explain availability: the feature, the tests, the review, the report\n")
    width = max(len(r["title"]) for r in res.rows)
    for r in res.rows:
        print(("%-6s %-4s %-*s  %s" % (r["verdict"], r["id"], width, r["title"], r["message"])).rstrip())
    print("-" * 78)
    print("SUMMARY pass=%d fail=%d error=%d   (%d checks)"
          % (counts["PASS"], counts["FAIL"], counts["ERROR"], len(res.rows)))
    if counts["FAIL"] or counts["ERROR"]:
        print("Every FAIL or ERROR you keep goes in lab-report.md section 9 and in submission.yml known_fails.")
        print("One you report and explain costs you nothing extra. One you hide costs the whole criterion.")
    else:
        print("Files and shape are clean. Whether your explanations and fixes are good is the grader's reading, not this.")


def main():
    parser = argparse.ArgumentParser(description="Week 11 checker - run from inside week-11/")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args()

    if not os.path.isdir("tests") and not os.path.exists(REPORT) and not os.path.isdir(APP):
        message = "run this from inside your week-11/ folder:  cd week-11 && python tests/check_feature.py"
        print(json.dumps({"ok": False, "error": message}) if args.json else "ERROR: " + message)
        return 3

    res, measured = run()
    counts = res.counts()
    ok = counts["FAIL"] == 0 and counts["ERROR"] == 0
    if args.json:
        print(json.dumps({"ok": ok, "counts": counts, "total": len(res.rows),
                          "rows": res.rows, "measured": measured}, ensure_ascii=False, indent=2))
    else:
        print_human(res, measured)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
