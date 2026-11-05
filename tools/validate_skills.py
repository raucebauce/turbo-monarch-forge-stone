#!/usr/bin/env python3
"""Validate the EDGE skill set: source skills, Grok packaging, evals and zips.

Usage:
    python3 tools/validate_skills.py                 # check; exit 1 on any failure
    python3 tools/validate_skills.py --report PATH   # also write the creation report
"""
import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / "artifacts"
SRC = ART / "edge-skills"  # source of truth: plain SKILL.md per skill
CRE = ART / "created-skills"  # the same skills in Grok's packaging
BRIEFS = ROOT / "attachments" / "edge-skills-grok-briefs.md"
BUNDLE = ART / "edge-skills-v2.2-created.zip"
FILES = ["CHANGELOG.md", "SKILL.md", "evals/evals.json", "evals/triggers.json"]
INCLUDE = "Include: skill name, inputs (commit/PR/model_version/venue), verdict, evidence table, and `next:` line."
EVIDENCE = "- Evidence rows are `claim | file:line or URL | PASS/FAIL/WARN`. No claim without a location."


def parse_briefs():
    """{skill: (number, should_trigger, should_not_trigger, eval_count)} from the creation briefs."""
    briefs = {}
    for section in re.split(r"\n## (?=\d+\. )", BRIEFS.read_text(encoding="utf-8"))[1:]:
        number, name = re.match(r"(\d+)\. (\S+)", section).groups()

        def quoted(label):
            return re.findall(r'"([^"]+)"', re.search(rf"\*\*{label}:\*\* (.+)", section).group(1))

        evals = re.search(r"\*\*Evals:\*\* (.+)", section).group(1)
        briefs[name] = (int(number), quoted("Should trigger"), quoted("Should NOT trigger"),
                        len(re.findall(r"\([a-h]\) ", evals)))
    return briefs


def grok_format(skill_md):
    """Grok's import quotes the description, adds type/lifecycle keys and a trailing blank line."""
    end = skill_md.index("\n---\n", 4)
    front = []
    for line in skill_md[4:end].split("\n"):
        if line.startswith("description: "):
            value = line[len("description: "):].replace("\\", "\\\\").replace('"', '\\"')
            line = f'description: "{value}"'
        front.append(line)
    front += ["type: workflow", "lifecycle: active"]
    return "---\n" + "\n".join(front) + "\n---\n" + skill_md[end + 5:] + "\n"


def zip_members(path):
    with zipfile.ZipFile(path) as archive:
        return {info.filename: archive.read(info) for info in archive.infolist() if not info.is_dir()}


def check_skill(name, brief):
    """Return (problems, files_present, (should, should_not), eval_count) for one skill."""
    problems = []
    src = (SRC / name / "SKILL.md").read_text(encoding="utf-8")
    front = re.match(r"---\nname: (\S+)\ndescription: \S.*\n---\n", src)
    if not front or front.group(1) != name:
        problems.append("SKILL.md frontmatter: name must match the folder and a description is required")
    _, found, handoff = src.partition("\n## Output & handoff\n")
    written = re.search(r"Write the result to `([^`]+)`", handoff)
    docs = re.search(r"docs/[^\s`]+", written.group(1)) if written else None
    for ok, part in [(found, "the block itself"), (docs, "a docs/ path"),
                     (INCLUDE in handoff, "verdict, evidence table and next: line"),
                     ("changelog` row" in handoff, "the changelog row"),
                     ("- Hands off: " in handoff, "the next skill"), (EVIDENCE in handoff, "the evidence format")]:
        if not ok:
            problems.append(f"Output & handoff: missing {part}")

    pkg = CRE / name
    present = [f for f in FILES if (pkg / f).is_file()]
    if len(present) < len(FILES):
        return problems + [f"missing {', '.join(sorted(set(FILES) - set(present)))}"], len(present), (0, 0), 0
    if (pkg / "SKILL.md").read_text(encoding="utf-8") != grok_format(src):
        problems.append("created SKILL.md is not the source SKILL.md in Grok format")
    if "v2.1 — initial import from edge-skills-v2.1.zip" not in (pkg / "CHANGELOG.md").read_text(encoding="utf-8"):
        problems.append("CHANGELOG.md lacks the v2.1 import row")

    triggers = json.loads((pkg / "evals/triggers.json").read_text(encoding="utf-8"))["test_cases"]
    should = [t["input"] for t in triggers if t["should_trigger"]]
    should_not = [t["input"] for t in triggers if not t["should_trigger"]]
    if (should, should_not) != (brief[1], brief[2]):
        problems.append("triggers.json differs from the brief's should / should-not lists")

    evals = json.loads((pkg / "evals/evals.json").read_text(encoding="utf-8"))["test_cases"]
    if len(evals) != brief[3]:
        problems.append(f"{len(evals)} evals, the brief defines {brief[3]}")
    output_file = None
    if docs:
        pattern = "[^/]+".join(map(re.escape, re.split(r"\{[^}]+\}", docs.group(0))))
        output_file = re.compile(rf"Output file {pattern} (exists|updated)")
    for case in evals:
        assertions = case["assertions"]
        if not (output_file and any(output_file.fullmatch(a) for a in assertions)):
            problems.append(f"eval {case['name']}: no 'Output file <docs path> exists' assertion")
        if not any(a.startswith("Evidence table") for a in assertions):
            problems.append(f"eval {case['name']}: no evidence-table assertion")
        if "Has next: line" not in assertions:
            problems.append(f"eval {case['name']}: no 'Has next: line' assertion")

    archive = ART / f"{name}.zip"
    if not archive.is_file() or zip_members(archive) != {f: (pkg / f).read_bytes() for f in FILES}:
        problems.append(f"{archive.name} does not match {pkg.relative_to(ROOT)}/")
    return problems, len(present), (len(should), len(should_not)), len(evals)


def write_report(path, rows, failures):
    lines = ["# EDGE Skills v2.2 Creation Report", "",
             "Generated by `python3 tools/validate_skills.py --report artifacts/creation-report.md`.",
             f"Files per skill: {', '.join(FILES)}.", "",
             "| # | Skill | Files | Triggers (should / should not) | Evals | Static checks |",
             "|---|---|---|---|---|---|"]
    for number, name, problems, present, (should, should_not), evals in rows:
        lines.append(f"| {number} | {name} | {present}/{len(FILES)} | {should} / {should_not} | {evals} | "
                     f"{'FAIL' if problems else 'PASS'} |")
    lines += ["", f"Bundle `{BUNDLE.name}`, per-skill zips and README skill table: {'FAIL' if failures else 'PASS'}"]
    lines += [f"- {failure}" for failure in failures]
    for number, name, problems, *_ in rows:
        lines += [f"- {name}: {problem}" for problem in problems]
    total = sum(row[5] for row in rows)
    lines += ["", f"**Eval results.** PASS means every static check held: the packaged SKILL.md is the source "
              "SKILL.md in Grok format, the Output & handoff block is complete, triggers match the briefs, "
              "every eval asserts the common pass criteria (output file, evidence table, `next:` line), "
              f"and each zip matches its folder. The {total} evals are defined but not run: running them "
              "needs the EDGE app itself (its repo, `docs/` and `changelog` table).", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Validate the EDGE skill set.")
    parser.add_argument("--report", type=Path, help="also write the creation report to this markdown file")
    args = parser.parse_args()

    briefs = parse_briefs()
    names = sorted(briefs, key=lambda n: briefs[n][0])
    failures, rows = [], []
    for folder in (SRC, CRE):
        found = {p.name for p in folder.iterdir() if p.is_dir()}
        if found != set(briefs):
            failures.append(f"{folder.relative_to(ROOT)}/: missing {sorted(set(briefs) - found)}, "
                            f"unexpected {sorted(found - set(briefs))}")
    zips = {p.stem for p in ART.glob("*.zip")} - {BUNDLE.stem}
    if zips != set(briefs):
        failures.append(f"per-skill zips: missing {sorted(set(briefs) - zips)}, unexpected {sorted(zips - set(briefs))}")
    for name in names:
        if (SRC / name / "SKILL.md").is_file():
            rows.append((briefs[name][0], name, *check_skill(name, briefs[name])))
        else:
            rows.append((briefs[name][0], name, ["source SKILL.md missing"], 0, (0, 0), 0))
    expected = {f"{n}/{f}": (CRE / n / f).read_bytes() for n in names for f in FILES if (CRE / n / f).is_file()}
    if not BUNDLE.is_file() or zip_members(BUNDLE) != expected:
        failures.append(f"{BUNDLE.name} does not match {CRE.relative_to(ROOT)}/")
    readme = (SRC / "README.md").read_text(encoding="utf-8")
    unlisted = [n for n in names if f"| {n} |" not in readme]
    if unlisted:
        failures.append(f"README.md table is missing {unlisted}")

    for number, name, problems, *_ in rows:
        print(f"{'FAIL' if problems else 'PASS'}  {number:>2}. {name}")
        for problem in problems:
            print(f"        - {problem}")
    for failure in failures:
        print(f"FAIL  {failure}")
    if args.report:
        write_report(args.report, rows, failures)
    failed = failures or any(row[2] for row in rows)
    print(f"\n{'FAILED' if failed else 'All checks passed'}: {sum(not row[2] for row in rows)}/{len(rows)} skills clean, "
          f"{len(failures)} set-level failure(s)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
