#!/usr/bin/env python3
"""
check_sis.py - the SIS #05 checker. DO NOT EDIT: the grader runs its own copy over your files.

    python tests/check_sis.py          # from inside sis-05/
    python tests/check_sis.py --json   # machine-readable, for the grading pipeline

What it checks (23 checks):

    P1-P6    your project in project/: source and a README; clean; AGENTS.md (or CLAUDE.md) with the
             seven topics and the four forbidden actions; at least one test file
    R1-R2    the output you pasted: the baseline (2.3) and the final checks (8.3)
    L1-L15   report.md: setup, map and commands, weaknesses, acceptance criteria, AGENTS.md coverage,
             the pattern decision, the review, the register, the audit, two mitigations, the final
             checks, the safeguards, the release decision, the reflection, the AI appendix

It never runs your project, never runs your tests and never talks to an assistant. It reads files,
in any language. A clean run is the floor, not the grade.

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

PROJECT = "project"
EVIDENCE = "evidence"
REPORT = "report.md"

MAX_EXPORT_MB = 10
MIN_IMAGE_BYTES = 3000
WORDS_MIN, WORDS_MAX = 200, 300
DECISION_MIN, DECISION_MAX = 80, 150
MIN_FINDINGS, MIN_RISKS, MIN_CONFIRMED, MIN_CATEGORIES, MIN_EXCHANGES = 5, 5, 2, 3, 3

IGNORED_DIRS = (".git", ".bolt", ".vscode", ".idea", "__pycache__", "node_modules", "dist", "build", "coverage",
                "venv", ".venv", "env", "target", ".gradle", ".pytest_cache", ".mypy_cache")
CODE_EXT = (".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".java", ".kt", ".go", ".rs", ".cs", ".cpp", ".cc",
            ".c", ".h", ".hpp", ".rb", ".php", ".swift", ".dart", ".scala", ".vue", ".svelte", ".html", ".sql",
            ".sh", ".lua", ".ex", ".exs", ".fs", ".hs", ".clj", ".r", ".m")
TEST_FILE = re.compile(r"(^test_.*\.py$|.*_test\.(py|go|rb|exs)$|.*\.(test|spec)\.[cm]?[jt]sx?$|.*Tests?\.(java|kt|cs|swift)$|"
                       r".*_spec\.rb$|.*_test\.(cpp|cc|c)$|^test.*\.(cpp|cc|c)$)", re.I)

CATEGORIES = (("correct", "correctness"), ("maintain", "maintainability"), ("secur", "security"),
              ("depend", "dependency"), ("agent", "agent operations"))
LABELS = {"confirmed": "confirmed", "plausible": "plausible", "unverified": "plausible",
          "plausible / unverified": "plausible", "plausible/unverified": "plausible",
          "unsupported": "unsupported"}
RELEASE = {"go": "go", "conditional": "conditional", "no-go": "no-go", "nogo": "no-go", "no go": "no-go"}
KINDS = ("test", "lint", "type", "build", "run")
RESULTS = ("pass", "fail", "missing", "not run")
AUDIT_ROWS = ("1a", "1b", "1c", "1d", "2a", "2b", "2c", "3a", "3b", "3c", "3d")
LEVEL_ROWS = {1: ("1a", "1b", "1c", "1d"), 2: ("2a", "2b", "2c"), 3: ("3a", "3b", "3c", "3d")}
TOPICS = (("Purpose", r"purpose|overview|what (?:this|it) (?:is|does)|about"),
          ("Architecture", r"architecture|structure|modules?|layout|components?"),
          ("Setup", r"setup|set up|install|getting started|requirements|environment"),
          ("Safe commands", r"commands?|scripts?|how to run|running|usage"),
          ("Coding conventions", r"conventions?|style|coding|code rules|standards"),
          ("Test expectations", r"tests?|testing|verification|quality"),
          ("Forbidden actions", r"forbidden|never|prohibited|do not|don't|must not|not allowed|restrictions|boundaries"))
FORBIDDEN = (("secrets", r"secret|credential|token|api key|password|\.env\b"),
             ("production deployments", r"deploy|production|publish|release"),
             ("destructive commands", r"destructive|rm -rf|force[- ]push|--force|reset --hard|drop (?:table|database)|delete"),
             ("unreviewed dependency changes", r"dependenc|package|librar|npm install|pip install|upgrade"))
NEG = re.compile(r"\b(?:never|not|no|don't|do not|must not|mustn't|cannot|can't|forbidden|prohibited|"
                 r"without|avoid|refuse|disallowed|only after|only with|requires? (?:a )?(?:human )?(?:review|approval))\b|n't\b", re.I)
SECRET_LITERALS = re.compile(r"\bsk-(?:proj-|ant-)?[A-Za-z0-9_-]{20,}|\bAIza[0-9A-Za-z_-]{30,}|\bgh[pousr]_[A-Za-z0-9]{30,}|"
                             r"\bAKIA[0-9A-Z]{16}\b|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\bxox[baprs]-[A-Za-z0-9-]{20,}")
SAFEGUARDS = ("The task", "Isolation", "Allowed files", "Commands", "Time limit", "Prohibited operations",
              "Required artifacts", "Human approval")
EXCHANGE_ROWS = ("tool and date", "exact model", "prompt", "output i used", "problems", "changes", "verified")

TITLES = {
    "P1": "project/: source files and a README",
    "P2": "project/ is clean: no .env, dependencies, nested .git or keys; under %d MB" % MAX_EXPORT_MB,
    "P3": "project/AGENTS.md or CLAUDE.md exists",
    "P4": "AGENTS.md covers the seven topics",
    "P5": "AGENTS.md forbids secrets, deployment, destructive commands, unreviewed dependencies",
    "P6": "project/ has at least one test file",
    "R1": "report 2.3: the baseline output",
    "R2": "report 8.3: the final output",
    "L1": "report 1: project, stack, origin, baseline commit, assistant, model",
    "L2": "report 2.1-2.2: the repository map and 3+ commands with results",
    "L3": "report 2.4: 3+ weaknesses with evidence, fact or assumption",
    "L4": "report 2.5: 3-5 acceptance criteria with how each is checked",
    "L5": "report 3: the file, how the assistant reads it, where each topic is",
    "L6": "report 4: the problem, the pattern, the decision, the checks after",
    "L7": "report 5: read-only, the prompt, the answer, %d+ findings in %d+ categories" % (MIN_FINDINGS, MIN_CATEGORIES),
    "L8": "report 6: %d+ risks, %d confirmed, scores = L x I; the top two" % (MIN_RISKS, MIN_CONFIRMED),
    "L9": "report 7: eleven audit rows; the level by the 80% rule; gaps",
    "L10": "report 8.1-8.2, 8.4: two confirmed risks mitigated, diffs, residual scores",
    "L11": "report 8.3: what was not run",
    "L12": "report 9.1: the eight safeguards",
    "L13": "report 9.2: the decision, %d-%d words, two risk IDs" % (DECISION_MIN, DECISION_MAX),
    "L14": "report 10: the reflection, %d-%d words" % (WORDS_MIN, WORDS_MAX),
    "L15": "report 11: %d+ complete AI exchanges" % MIN_EXCHANGES,
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

PLACEHOLDER = re.compile(r"\(paste here\)|\(write here[^)]*\)|^<.*>$|yes / no|GO / CONDITIONAL / NO-GO|"
                         r"applied / not warranted|^\s*R\?\s*$|\(0, 1, 2 or 3", re.I)


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




def is_real_output(text):
    """Pasted terminal output, not a placeholder or a sentence: 3+ non-empty lines."""
    text = (text or "").strip()
    return bool(text) and not PLACEHOLDER.search(text) and len([l for l in text.splitlines() if l.strip()]) >= 3


def project_files():
    return list(walk_files(PROJECT)) if os.path.isdir(PROJECT) else []


def agents_file():
    for name in ("AGENTS.md", "CLAUDE.md", "agents.md", "claude.md"):
        p = os.path.join(PROJECT, name)
        if os.path.isfile(p):
            return p
    return None


# --------------------------------------------------------------------------- P: the project


def check_project(res, measured):
    files = project_files()
    measured["project_files"] = len(files)
    code = [p for p in files if p.lower().endswith(CODE_EXT)]
    readme = [p for p in files if os.path.basename(p).lower().startswith("readme") and os.path.dirname(p) == PROJECT]
    if not os.path.isdir(PROJECT) or not files:
        res.add("P1", "ERROR", "project/ is empty or missing - copy your project in (README section 3)")
    else:
        miss = ([] if code else ["source files"]) + ([] if readme else ["a README at project/"])
        res.add("P1", "FAIL" if miss else "PASS", "project/ needs " + " and ".join(miss) if miss
                else "%d source files, %s" % (len(code), rel(readme[0])))

    probs, size = [], 0
    if os.path.isdir(PROJECT):
        for here, dirs, names in os.walk(PROJECT):
            for d in list(dirs):
                if d in ("node_modules", "venv", ".venv", ".git", "__pycache__", "target", ".gradle"):
                    if d not in ("__pycache__",):
                        probs.append("%s/%s must not be committed" % (rel(here), d))
                    dirs.remove(d)
            for n in names:
                p = os.path.join(here, n)
                if n == ".env" or (n.startswith(".env.") and n not in (".env.example", ".env.sample")):
                    probs.append("%s must not be committed" % rel(p))
                try:
                    size += os.path.getsize(p)
                except OSError:
                    pass
                if os.path.getsize(p) < 2 * 1024 * 1024 and SECRET_LITERALS.search(read(p) or ""):
                    probs.append("a key-like string in %s" % rel(p))
        if size > MAX_EXPORT_MB * 1024 * 1024:
            probs.append("project/ is %.1f MB - source, tests, config and docs only" % (size / 1048576.0))
    if not files:
        res.add("P2", "ERROR", "nothing to check until project/ holds the project")
    else:
        res.add("P2", "FAIL" if probs else "PASS", "; ".join(probs[:4]) if probs else "clean")

    tests = [p for p in files if TEST_FILE.match(os.path.basename(p)) or "/tests/" in rel(p) + "/" and p.lower().endswith(CODE_EXT)
             or "/test/" in rel(p) and p.lower().endswith(CODE_EXT)]
    measured["test_files"] = [rel(p) for p in tests[:10]]
    if not files:
        res.add("P6", "ERROR", "no project to look in")
    else:
        res.add("P6", "PASS" if tests else "FAIL", "%d test file(s), e.g. %s" % (len(tests), rel(tests[0])) if tests
                else "no test file in project/ - Task 7 adds at least one (README section 11)")

    agents = agents_file()
    measured["agents_file"] = rel(agents)
    if not agents:
        res.add("P3", "ERROR" if not files else "FAIL", "no AGENTS.md or CLAUDE.md at project/ (README section 6)")
        res.add("P4", "ERROR", "no AGENTS.md to read")
        res.add("P5", "ERROR", "no AGENTS.md to read")
        return
    res.add("P3", "PASS", rel(agents))
    text = read(agents) or ""
    heads = " ".join(l for l in text.splitlines() if l.lstrip().startswith("#")).lower()
    lacking = [name for name, pat in TOPICS if not re.search(pat, heads, re.I)]
    res.add("P4", "FAIL" if lacking else "PASS", "no heading for: " + ", ".join(lacking) if lacking
            else "seven topics under headings")
    lines = [l for l in text.splitlines() if l.strip() and not l.lstrip().startswith("#")]
    missing = [name for name, pat in FORBIDDEN if not any(re.search(pat, l, re.I) and NEG.search(l) for l in lines)]
    res.add("P5", "FAIL" if missing else "PASS", "no line forbids: " + ", ".join(missing) if missing
            else "the four forbidden actions are stated")


# --------------------------------------------------------------------------- L: the report


def check_setup(res, measured, sec):
    rows = [(clean_cell(r[0]).lower(), r[1]) for r in table_rows(sec.get("1", "")) if len(r) > 1]
    need = (("project", "the project"), ("language", "the language and stack"), ("comes from", "where it comes from"),
            ("baseline commit", "the baseline commit"), ("assistant", "the assistant"), ("exact model", "the exact model"),
            ("ran the commands", "where you ran the commands"))
    lacking = [say for key, say in need if not any(key in k and useful(v) for k, v in rows)]
    commit = next((clean_cell(v) for k, v in rows if "baseline commit" in k), "")
    m = re.search(r"\b[0-9a-f]{7,40}\b", commit)
    if commit and useful(commit) and not m:
        lacking.append("the baseline commit as a hash")
    measured["baseline_commit"] = m.group(0) if m else None
    res.add("L1", "FAIL" if lacking else "PASS", "section 1 needs: " + ", ".join(lacking) if lacking else "setup recorded")


def check_baseline(res, measured, sec):
    probs = []
    rows = {clean_cell(r[0]).lower(): r for r in table_rows(sec.get("2.1", "")) if r}
    for part in ("entry points", "modules", "dependencies", "tests", "build"):
        r = next((v for k, v in rows.items() if k.startswith(part)), None)
        if not r or len(r) < 2 or not useful(r[1]):
            probs.append("2.1: " + part)
    cmds = [r for r in table_rows(sec.get("2.2", "")) if len(r) >= 4 and useful(r[0]) and clean_cell(r[0]).lower() != "command"
            and clean_cell(r[1]).lower() in KINDS and clean_cell(r[2]).lower() in ("yes", "no")
            and clean_cell(r[3]).lower() in RESULTS]
    measured["commands"] = len(cmds)
    if len(cmds) < 3:
        probs.append("2.2: three or more commands with kind, exists and result (found %d)" % len(cmds))
    res.add("L2", "FAIL" if probs else "PASS", "section " + "; ".join(probs) if probs
            else "map filled, %d commands" % len(cmds))

    out = " \n".join(blocks(sec.get("2.3", "")))
    res.add("R1", "PASS" if is_real_output(out) else "FAIL", "baseline output pasted" if is_real_output(out)
            else "section 2.3 needs the real output of the baseline run (3+ lines)")

    good = [r for r in table_rows(sec.get("2.4", "")) if len(r) >= 4 and re.match(r"^\d+$", clean_cell(r[0]))
            and useful(r[1]) and useful(r[2]) and clean_cell(r[3]).lower() in ("fact", "assumption")]
    res.add("L3", "PASS" if len(good) >= 3 else "FAIL", "%d weaknesses with evidence" % len(good) if len(good) >= 3
            else "section 2.4: 3+ weaknesses, each with evidence and fact / assumption (found %d)" % len(good))

    acs = [r for r in table_rows(sec.get("2.5", "")) if len(r) >= 3 and re.match(r"^AC[1-5]$", clean_cell(r[0]))
           and useful(r[1]) and useful(r[2])]
    measured["acceptance_criteria"] = len(acs)
    ok = 3 <= len(acs) <= 5
    res.add("L4", "PASS" if ok else "FAIL", "%d acceptance criteria" % len(acs) if ok
            else "section 2.5: 3-5 criteria (AC1-AC5), each with how you check it (found %d)" % len(acs))


def check_agents_report(res, sec):
    probs = []
    rows = {clean_cell(r[0]).lower(): r for r in table_rows(sec.get("3.1", "")) if r}
    for key, say in (("file", "the file"), ("created or improved", "created or improved"), ("load it", "whether it loads it")):
        r = next((v for k, v in rows.items() if k.startswith(key) or key in k), None)
        if not r or len(r) < 2 or not useful(r[1]):
            probs.append("3.1: " + say)
    cov = {clean_cell(r[0]).lower(): r for r in table_rows(sec.get("3.2", "")) if r}
    thin = [name for name, _ in TOPICS if not (cov.get(name.lower()) and len(cov[name.lower()]) > 1 and useful(cov[name.lower()][1]))]
    if thin:
        probs.append("3.2: where to find " + ", ".join(thin))
    res.add("L5", "FAIL" if probs else "PASS", "section " + "; ".join(probs) if probs else "file, loading, seven topics located")


def check_pattern(res, sec):
    probs = []
    if word_count(after_marker(sec.get("4.1", ""))) < 15:
        probs.append("4.1: the problem, located (15+ words)")
    if word_count(after_marker(sec.get("4.2", ""))) < 15:
        probs.append("4.2: the pattern you evaluated (15+ words)")
    body = strip_comments(sec.get("4.3", ""))
    m = re.search(r"Decision:\**\s*\**\s*(applied|not warranted)\b(?!\s*/)", body, re.I)
    if not m:
        probs.append("4.3: one decision after **Decision:** - applied or not warranted")
    if word_count(after_marker(sec.get("4.3", ""))) < 20:
        probs.append("4.3: why, and before / after (20+ words)")
    if not is_real_output(" \n".join(blocks(sec.get("4.4", "")))):
        probs.append("4.4: the real output of the checks after the decision")
    res.add("L6", "FAIL" if probs else "PASS", "section " + "; ".join(probs) if probs
            else "problem, pattern, %s, checks after" % m.group(1).lower())


def check_review(res, measured, sec):
    probs = []
    s51 = sec.get("5.1", "")
    if word_count(after_marker(s51).split("What you sent")[0]) < 10:
        probs.append("5.1: how it could not modify files, and what it was given (10+ words)")
    b = blocks(s51)
    sent = b[0] if b else ""
    if PLACEHOLDER.search(sent) or len(norm(sent).split()) < 15:
        probs.append("5.1: the prompt as sent (15+ words)")
    elif not re.search(r"\b(?:not|never|don't|do not|without)\b[^.]{0,40}\b(?:modif|edit|chang|writ)", sent, re.I):
        probs.append("5.1: the prompt must say the assistant may not modify files")
    if len(b) < 2 or PLACEHOLDER.search(b[1]) or len(norm(b[1]).split()) < 50:
        probs.append("5.1: the answer (50+ words)")
    good, cats = 0, set()
    for r in table_rows(sec.get("5.2", "")):
        if len(r) < 6 or not re.match(r"^\d+$", clean_cell(r[0])):
            continue
        cat = category_of(r[2])
        if useful(r[1]) and cat and useful(r[3]) and LABELS.get(clean_cell(r[4]).lower()) and useful(r[5]):
            good += 1
            cats.add(cat)
    measured["findings"] = good
    if good < MIN_FINDINGS:
        probs.append("5.2: %d complete findings, %d needed" % (good, MIN_FINDINGS))
    if len(cats) < MIN_CATEGORIES:
        probs.append("5.2: %d categories, %d needed" % (len(cats), MIN_CATEGORIES))
    res.add("L7", "FAIL" if probs else "PASS", "section " + "; ".join(probs[:3]) if probs
            else "read-only, prompt, answer, %d findings in %d categories" % (good, len(cats)))


def component_real(cell):
    c = clean_cell(cell)
    if re.match(r"^missing\b", c, re.I):
        return len(c.split()) >= 2
    names = set(os.path.relpath(p, PROJECT).replace(os.sep, "/") for p in project_files())
    bases = set(os.path.basename(n) for n in names)
    for tok in re.findall(r"[\w./-]+\.[A-Za-z0-9]{1,5}\b", c):
        tok = tok.lstrip("./")
        if tok.startswith("project/"):
            tok = tok[8:]
        if tok in names or os.path.basename(tok) in bases:
            return True
    return False


def check_register(res, measured, sec):
    register, probs, cats = {}, [], set()
    for r in table_rows(sec.get("6.1", "")):
        if not r or not re.match(r"^R\d{1,2}$", clean_cell(r[0])) or len(r) < 12 or not any(useful(c) for c in r[1:]):
            continue
        rid = clean_cell(r[0])
        miss = [n for n, c in zip(("category", "cause", "component", "evidence", "status", "L", "I", "score",
                                   "mitigation", "owner", "verification plan"), r[1:12]) if not useful(c)]
        status = LABELS.get(clean_cell(r[5]).lower())
        lv, iv, sc = as_int(r[6]), as_int(r[7]), as_int(r[8])
        register[rid] = {"status": status, "L": lv, "I": iv, "score": sc}
        if miss:
            probs.append("%s: empty %s" % (rid, ", ".join(miss)))
            continue
        cat = category_of(r[1])
        if cat:
            cats.add(cat)
        else:
            probs.append("%s: category is one of the five" % rid)
        if status not in ("confirmed", "plausible"):
            probs.append("%s: status is confirmed or plausible" % rid)
        if lv not in (1, 2, 3) or iv not in (1, 2, 3):
            probs.append("%s: L and I are 1-3" % rid)
        elif sc != lv * iv:
            probs.append("%s: score %s is not %d x %d" % (rid, clean_cell(r[8]), lv, iv))
        if not component_real(r[3]):
            probs.append("%s: component \"%s\" is not a file in project/ nor 'missing: <check>'" % (rid, clean_cell(r[3])[:40]))
    confirmed = [k for k, v in register.items() if v["status"] == "confirmed"]
    measured["risks"] = len(register)
    measured["risks_confirmed"] = len(confirmed)
    if len(register) < MIN_RISKS:
        probs.insert(0, "%d risks, %d needed" % (len(register), MIN_RISKS))
    if len(confirmed) < MIN_CONFIRMED:
        probs.append("%d confirmed, %d needed" % (len(confirmed), MIN_CONFIRMED))
    if len(cats) < MIN_CATEGORIES:
        probs.append("%d categories, %d needed" % (len(cats), MIN_CATEGORIES))
    lines = [l for l in strip_comments(sec.get("6.2", "")).splitlines() if re.match(r"^\s*[12]\.", l)]
    top = [("R" + risk_ids(l)[0], len(re.findall(r"[^\W_]+", re.sub(r"R\d+", " ", l))) - 1) for l in lines if risk_ids(l)]
    measured["top_two"] = [t for t, _ in top[:2]]
    if len(top) < 2:
        probs.append("6.2: two risk IDs, one per line")
    else:
        (a, wa), (b, wb) = top[:2]
        for rid in (a, b):
            if register.get(rid, {}).get("status") != "confirmed":
                probs.append("6.2: %s is not a confirmed risk in 6.1" % rid)
        if a == b:
            probs.append("6.2: two different risks")
        if min(wa, wb) < 6:
            probs.append("6.2: the evidence that justifies each score (6+ words each)")
        if a in register and b in register and (register[a]["score"] or 0) < (register[b]["score"] or 0):
            probs.append("6.2: highest score first")
        second = min(register.get(a, {}).get("score") or 0, register.get(b, {}).get("score") or 0)
        higher = [k for k in confirmed if k not in (a, b) and (register[k]["score"] or 0) > second]
        if higher:
            probs.append("6.2: %s is confirmed and scores higher than your second" % higher[0])
    res.add("L8", "FAIL" if probs else "PASS", "section 6: " + "; ".join(probs[:3]) +
            (" (+%d more)" % (len(probs) - 3) if len(probs) > 3 else "") if probs
            else "%d risks, %d confirmed, %d categories, top two %s" % (len(register), len(confirmed), len(cats), ", ".join(measured["top_two"])))
    return register


def check_audit(res, measured, sec):
    rows = {clean_cell(r[0]).lower(): r for r in table_rows(sec.get("7.1", "")) if r}
    answers, bad = {}, []
    for rid in AUDIT_ROWS:
        r = rows.get(rid)
        ans = clean_cell(r[2]).lower() if r and len(r) >= 4 else ""
        if ans not in ("yes", "no") or not useful(r[3]):
            bad.append(rid)
        else:
            answers[rid] = ans == "yes"
    computed = None
    if not bad:
        computed = 0
        for lvl in (1, 2, 3):
            rws = LEVEL_ROWS[lvl]
            if sum(answers[x] for x in rws) / float(len(rws)) >= 0.8:
                computed = lvl
            else:
                break
    body = strip_comments(sec.get("7.2", ""))
    m = re.search(r"Level:\**\s*\**\s*([0-3])\b", body)
    measured["level_declared"] = int(m.group(1)) if m else None
    measured["level_computed"] = computed
    agents = agents_file()
    probs = []
    if bad:
        probs.append("7.1: yes / no and the evidence for rows " + ", ".join(bad))
    elif answers.get("2c") and not agents:
        probs.append("7.1: 2c says yes, but project/ has no AGENTS.md")
    if not m:
        probs.append("7.2: the level as one digit after **Level:**")
    elif computed is not None and int(m.group(1)) != computed:
        probs.append("7.2: your rows give Level %d by the 80%% rule, not %s" % (computed, m.group(1)))
    gaps = word_count(body.split("Missing evidence", 1)[1]) if "Missing evidence" in body else 0
    if gaps < 10 and not (m and m.group(1) == "3"):
        probs.append("7.2: the missing evidence for the next level (10+ words)")
    res.add("L9", "FAIL" if probs else "PASS", "section " + "; ".join(probs) if probs else "eleven rows, Level %d, gaps named" % computed)


def check_mitigations(res, measured, sec, register):
    ids, probs = [], []
    for key in ("8.1", "8.2"):
        body = strip_comments(sec.get(key, ""))
        m = re.search(r"Risk:\**\s*\**\s*(R\d{1,2})\b", body)
        rid = m.group(1) if m else None
        ids.append(rid)
        if not rid:
            probs.append("%s: the risk ID (**Risk:** R1)" % key)
            continue
        if register.get(rid, {}).get("status") != "confirmed":
            probs.append("%s: %s is not a confirmed risk in 6.1" % (key, rid))
        what = body.split("from the assistant's proposal:", 1)[1].split("The test that fails", 1)[0] \
            if "from the assistant's proposal:" in body else ""
        if word_count(what) < 10:
            probs.append("%s: what you changed and what you rejected (10+ words)" % key)
        bl = blocks(sec.get(key, ""))
        test = bl[0] if bl else ""
        if PLACEHOLDER.search(test) or len(norm(test).split()) < 8:
            probs.append("%s: the failing test run, or why a test is not feasible" % key)
        if not is_diff(" \n".join(bl[1:])):
            probs.append("%s: the diff" % key)
    if ids[0] and ids[0] == ids[1]:
        probs.append("two different risks")
    after = {}
    for r in table_rows(sec.get("8.4", "")):
        if len(r) < 8 or not re.match(r"^R\d{1,2}$", clean_cell(r[0])):
            continue
        rid = clean_cell(r[0])
        nums = [as_int(c) for c in r[1:7]]
        if None in nums or not useful(r[7]):
            probs.append("8.4: %s needs six numbers and the evidence" % rid)
            continue
        lb, ib, sb, la, ia, sa = nums
        reg = register.get(rid)
        if reg and (lb, ib, sb) != (reg["L"], reg["I"], reg["score"]):
            probs.append("8.4: %s before (%d x %d = %d) differs from the register" % (rid, lb, ib, sb))
        if la not in (1, 2, 3) or ia not in (1, 2, 3) or sa != la * ia:
            probs.append("8.4: %s after must be L x I with L and I 1-3" % rid)
        elif sa > sb:
            probs.append("8.4: %s scores higher after the mitigation" % rid)
        after[rid] = sa
    for rid in ids:
        if rid and rid not in after and not any(p.startswith("8.4: %s" % rid) for p in probs):
            probs.append("8.4: a row for %s" % rid)
    if word_count(after_marker(sec.get("8.4", ""))) < 10:
        probs.append("8.4: the remaining limitations (10+ words)")
    measured["mitigated"] = [i for i in ids if i]
    res.add("L10", "FAIL" if probs else "PASS", "section " + "; ".join(probs[:3]) +
            (" (+%d more)" % (len(probs) - 3) if len(probs) > 3 else "") if probs
            else "%s and %s mitigated, scores revised" % tuple(ids))

    out = " \n".join(blocks(sec.get("8.3", "")))
    res.add("R2", "PASS" if is_real_output(out) else "FAIL", "final output pasted" if is_real_output(out)
            else "section 8.3 needs the real output of the final run (3+ lines)")
    tail = strip_comments(sec.get("8.3", "")).split("```")[-1]
    notrun = word_count(tail.split("did not run, and why:", 1)[-1])
    res.add("L11", "PASS" if notrun >= 1 else "FAIL", "tests not run listed" if notrun >= 1
            else "section 8.3: list the tests and checks you did not run, or none")
    return after


def check_release(res, measured, sec, register, after):
    rows = {clean_cell(r[0]).lower(): r for r in table_rows(sec.get("9.1", "")) if r}
    thin = []
    for name in SAFEGUARDS:
        r = next((v for k, v in rows.items() if k.startswith(name.lower())), None)
        if not r or len(r) < 2 or not useful(r[1]) or len(re.findall(r"[^\W_]+", clean_cell(r[1]))) < 4:
            thin.append(name)
    res.add("L12", "FAIL" if thin else "PASS", "section 9.1: 4+ words for " + ", ".join(thin) if thin else "eight safeguards")

    body = sec.get("9.2", "")
    m = re.search(r"Decision:\**\s*\**\s*([A-Za-z -]+?)\s*(?:\*\*|$)", strip_comments(body), re.M)
    word = RELEASE.get(m.group(1).strip().lower()) if m else None
    measured["release"] = word
    current = {k: after.get(k, v["score"] or 0) for k, v in register.items() if v["status"] == "confirmed"}
    high = sorted(k for k, s in current.items() if s >= 6)
    text = after_marker(body, "Write your justification below this line")
    words = word_count(text)
    named = sorted(set("R" + i for i in risk_ids(strip_comments(text))) & set(register))
    probs = []
    if not word:
        probs.append("one decision after **Decision:** - GO, CONDITIONAL or NO-GO")
    elif word == "go" and high:
        probs.append("GO is not allowed while %s still score 6 or more" % ", ".join(high))
    if not DECISION_MIN <= words <= DECISION_MAX:
        probs.append("%d words, the task asks for %d-%d" % (words, DECISION_MIN, DECISION_MAX))
    if len(named) < 2:
        probs.append("name two or more risk IDs from your register")
    res.add("L13", "FAIL" if probs else "PASS", "section 9.2: " + "; ".join(probs) if probs
            else "%s, %d words, %s" % (word.upper(), words, ", ".join(named[:4])))


def check_reflection(res, measured, sec):
    words = word_count(after_marker(sec.get("10", ""), "Write your reflection below this line"))
    measured["reflection_words"] = words
    ok = WORDS_MIN <= words <= WORDS_MAX
    res.add("L14", "PASS" if ok else "FAIL", "%d words" % words if ok
            else "section 10: %d words, the task asks for %d-%d" % (words, WORDS_MIN, WORDS_MAX))


def check_appendix(res, measured, sec):
    complete = 0
    for key in sorted(k for k in sec if re.match(r"^11\.\d+$", k)):
        rows = {clean_cell(r[0]).lower(): r for r in table_rows(sec[key]) if r}
        if not rows:
            continue
        if all(any(want in k and len(r) > 1 and useful(r[1]) for k, r in rows.items()) for want in EXCHANGE_ROWS):
            complete += 1
    measured["exchanges"] = complete
    res.add("L15", "PASS" if complete >= MIN_EXCHANGES else "FAIL", "%d complete exchanges" % complete
            if complete >= MIN_EXCHANGES else "section 11: %d complete exchanges (all seven rows), %d needed" % (complete, MIN_EXCHANGES))


# --------------------------------------------------------------------------- main


def run():
    res, measured = Results(), {}
    check_project(res, measured)
    text = read(REPORT)
    if text is None:
        for cid in ORDER:
            if cid[0] in "RL":
                res.add(cid, "ERROR", "report.md not found")
    else:
        sec = sections(text)
        check_setup(res, measured, sec)
        check_baseline(res, measured, sec)
        check_agents_report(res, sec)
        check_pattern(res, sec)
        check_review(res, measured, sec)
        register = check_register(res, measured, sec)
        check_audit(res, measured, sec)
        after = check_mitigations(res, measured, sec, register)
        check_release(res, measured, sec, register, after)
        check_reflection(res, measured, sec)
        check_appendix(res, measured, sec)
    res.rows = sorted(res.rows, key=lambda r: ORDER.index(r["id"]))
    return res, measured


def print_human(res, measured):
    counts = res.counts()
    print("SIS #05 - repository customization, agent readiness and risk governance\n")
    width = max(len(r["title"]) for r in res.rows)
    for r in res.rows:
        print(("%-6s %-4s %-*s  %s" % (r["verdict"], r["id"], width, r["title"], r["message"])).rstrip())
    print("-" * 78)
    print("SUMMARY pass=%d fail=%d error=%d   (%d checks)"
          % (counts["PASS"], counts["FAIL"], counts["ERROR"], len(res.rows)))
    if counts["FAIL"] or counts["ERROR"]:
        print("Every FAIL or ERROR you keep goes in report.md section 11.4 and in submission.yml known_fails.")
        print("One you report and explain costs you nothing. One you hide costs the whole criterion.")
    else:
        print("Files and shape are clean. Whether your risks and decisions are right is the grader's reading, not this.")


def main():
    parser = argparse.ArgumentParser(description="SIS #05 checker - run from inside sis-05/")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args()

    if not os.path.isdir("tests") and not os.path.exists(REPORT) and not os.path.isdir(PROJECT):
        message = "run this from inside your sis-05/ folder:  cd sis-05 && python tests/check_sis.py"
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
