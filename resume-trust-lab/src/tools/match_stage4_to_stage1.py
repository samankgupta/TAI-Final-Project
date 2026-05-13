"""Create CSV by matching `outputs/stage_4.json` ranked candidate_ids
to `outputs/stage_1.json` resumes.

Usage:
  python match_stage4_to_stage1.py
Outputs:
  resume-trust-lab/outputs/stage_4_expanded.csv
"""
import json
import csv
from pathlib import Path
import csv as _csv

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / 'outputs'
STAGE4 = OUT_DIR / 'stage_4.json'
STAGE1 = OUT_DIR / 'stage_1.json'
OUT_CSV = OUT_DIR / 'stage_4_expanded_full.csv'
import sys

# Try to locate dataset.csv in likely locations (avoid importing project dependencies)
POSSIBLE = [
    ROOT.parent / 'dataset.csv',
    ROOT / 'dataset.csv',
    ROOT.parent.parent / 'dataset.csv'
]

DATASET_PATH = None
for p in POSSIBLE:
    if p.exists():
        DATASET_PATH = str(p)
        break

if DATASET_PATH is None:
    # Fallback: try to parse config.py for DATASET_PATH string literal
    cfg = ROOT / 'src' / 'config.py'
    if cfg.exists():
        import re
        txt = cfg.read_text()
        m = re.search(r"DATASET_PATH\s*=\s*['\"]([^'\"]+)['\"]", txt)
        if m:
            DATASET_PATH = m.group(1)

if DATASET_PATH is None:
    raise FileNotFoundError('Could not locate dataset.csv; please set its path in the script')


def load_json(path: Path):
    with open(path, 'r') as f:
        return json.load(f)


def main():
    if not STAGE4.exists():
        print(f"Missing {STAGE4}")
        return
    if not STAGE1.exists():
        print(f"Missing {STAGE1}")
        return

    s4 = load_json(STAGE4)
    s1 = load_json(STAGE1)

    # read dataset and reconstruct the filtered list used in stage 1
    role = s1.get('parameters', {}).get('role') or ''
    max_matches = s1.get('parameters', {}).get('max_role_matches')

    # Read dataset.csv without pandas to avoid dependency issues
    id_map = {}
    try:
        with open(DATASET_PATH, newline='', encoding='utf-8') as csvfile:
            reader = _csv.DictReader(csvfile)
            matched = [r for r in reader if (r.get('Role') or '').lower() == (role or '').lower()]
    except Exception as e:
        print(f"Error reading dataset at {DATASET_PATH}: {e}")
        matched = []

    if max_matches is not None and matched and len(matched) > int(max_matches):
        matched = matched[:int(max_matches)]

    for idx, r in enumerate(matched):
        id_map[idx] = {'role': r.get('Role', ''), 'resume_full': r.get('Resume', '')}

    rows = []
    for item in s4.get('ranked_resumes', []):
        cid = item.get('candidate_id')
        entry = id_map.get(cid, {})
        rows.append({
            'rank': item.get('rank'),
            'candidate_id': cid,
            'gemini_score': item.get('gemini_score'),
            'reasoning': item.get('reasoning'),
            'role': entry.get('role', ''),
            'resume': entry.get('resume_full', ''),
        })

    # write CSV
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['rank', 'candidate_id', 'gemini_score', 'reasoning', 'role', 'resume']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    print(f"Wrote {len(rows)} rows to {OUT_CSV}")


if __name__ == '__main__':
    main()
