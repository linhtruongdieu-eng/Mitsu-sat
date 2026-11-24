#!/usr/bin/env python3
"""Phân tích câu sai SAT: thống kê theo domain, kỹ năng, nguyên nhân sai,
đối chiếu với bảng điểm thi thật.

Cách dùng:
    python3 tools/analyze.py                 # in báo cáo ra màn hình
    python3 tools/analyze.py --since 2026-11-01   # chỉ tính câu sai từ ngày này

Dữ liệu:
    data/wrong_answers.csv   - mỗi dòng là một câu sai (thêm dòng mới hằng ngày)
    data/score_reports.csv   - mỗi dòng là một lần thi thật
"""
import argparse
import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

CAUSE_LABELS = {
    "concept": "Hổng kiến thức / quy tắc",
    "trap": "Sa bẫy đáp án gần đúng",
    "off_goal": "Lệch mục tiêu câu hỏi (đáp án đúng sự thật nhưng không trả lời đề)",
    "misread": "Đọc sai / bỏ sót dữ kiện",
    "vocab": "Từ vựng / nghĩa trong ngữ cảnh",
    "careless": "Cẩu thả khi tính",
    "blank": "Bỏ trống / không kịp làm",
}

# Domain trên bảng điểm College Board -> cột trong score_reports.csv
DOMAIN_COLS = {
    "Information and Ideas": "info_ideas",
    "Craft and Structure": "craft_structure",
    "Expression of Ideas": "expression_ideas",
    "Standard English Conventions": "sec",
    "Algebra": "algebra",
    "Advanced Math": "advanced_math",
    "Problem-Solving and Data Analysis": "psda",
    "Geometry & Trigonometry": "geo_trig",
}


def load(name):
    with open(DATA / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def bar(n, total, width=24):
    filled = round(width * n / total) if total else 0
    return "█" * filled + "·" * (width - filled)


def table(counter, total, labels=None):
    lines = []
    for key, n in counter.most_common():
        label = (labels or {}).get(key, key)
        lines.append(f"  {bar(n, total)} {n:>3} ({n / total:5.1%})  {label}")
    return "\n".join(lines)


def repeated(rows):
    """Tiểu kỹ năng sai >= 2 lần với cùng nguyên nhân: dấu hiệu chưa ôn lỗi cũ."""
    c = Counter((r["subskill"], r["error_cause"]) for r in rows)
    return [(k, n) for k, n in c.most_common() if n >= 2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", help="YYYY-MM-DD: chỉ tính câu sai có date >= ngày này")
    args = ap.parse_args()

    rows = load("wrong_answers.csv")
    if args.since:
        rows = [r for r in rows if r["date"] and r["date"] >= args.since]
    scores = load("score_reports.csv")

    print("=== BẢNG ĐIỂM THI THẬT ===")
    for s in scores:
        print(f"  {s['date']}: Total {s['total']} | R&W {s['rw']} | Math {s['math']}")
    if len(scores) >= 2:
        a, b = scores[0], scores[-1]
        print(f"  Thay đổi: Total {int(b['total']) - int(a['total']):+d}, "
              f"R&W {int(b['rw']) - int(a['rw']):+d}, Math {int(b['math']) - int(a['math']):+d}")

    total = len(rows)
    print(f"\n=== CÂU SAI: {total} câu ===")
    for section in ("RW", "Math"):
        sec_rows = [r for r in rows if r["section"] == section]
        if not sec_rows:
            continue
        n = len(sec_rows)
        print(f"\n--- {section}: {n} câu ---")
        print("Theo domain (kèm băng điểm lần thi đầu → gần nhất):")
        dc = Counter(r["domain"] for r in sec_rows)
        for dom, k in dc.most_common():
            col = DOMAIN_COLS.get(dom)
            band = f"  [{scores[0][col]} → {scores[-1][col]}]" if col and scores else ""
            print(f"  {bar(k, n)} {k:>3} ({k / n:5.1%})  {dom}{band}")
        print("Theo tiểu kỹ năng:")
        print(table(Counter(r["subskill"] for r in sec_rows), n))
        print("Theo nguyên nhân sai:")
        print(table(Counter(r["error_cause"] for r in sec_rows), n, CAUSE_LABELS))

    print("\n=== LỖI LẶP LẠI (cùng tiểu kỹ năng + cùng nguyên nhân, >= 2 lần) ===")
    for (skill, cause), n in repeated(rows):
        print(f"  {n}x  {skill}  —  {CAUSE_LABELS.get(cause, cause)}")


if __name__ == "__main__":
    main()
