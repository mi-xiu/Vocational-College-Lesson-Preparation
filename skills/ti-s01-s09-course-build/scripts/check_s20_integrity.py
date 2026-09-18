#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# S20 对齐产物全面核查脚本（只读，不改动任何文件）
# 通用版：针对任意高职课程的 S20 模板对齐产物固化；通过 --base 与 --course-name 适配不同课程。
# 用法：python3 scripts/check_s20_integrity.py --base /path/to/课程根 --course-name <课程名>
import os, re, argparse
from docx import Document
from openpyxl import load_workbook

parser = argparse.ArgumentParser(description="核查 S20 对齐产物完整性与一致性")
parser.add_argument("--base", default="/Users/a1-6/WorkBuddy",
                    help="课程根目录（含 01_.. 各 S 步目录与 09_S20模板缺口分析）")
parser.add_argument("--course-name", default="course",
                    help="课程名，用于推导课程标准/整体设计/授课计划等文件名")
args = parser.parse_args()
BASE = args.base
COURSE = args.course_name
issues = []
ok = []

def check(cond, msg):
    (ok if cond else issues).append(msg)

# ---------- 1. office 骨架 19 文件可打开 ----------
OD = os.path.join(BASE, "09_S20模板缺口分析/blank_skeletons_office")
n_docx = n_xlsx = 0
for root, _, files in os.walk(OD):
    for f in files:
        p = os.path.join(root, f)
        if f.endswith(".docx"):
            n_docx += 1
            try:
                Document(p)
            except Exception as e:
                issues.append(f"[OFFICE损坏] {f}: {e}")
        elif f.endswith(".xlsx"):
            n_xlsx += 1
            try:
                load_workbook(p)
            except Exception as e:
                issues.append(f"[OFFICE损坏] {f}: {e}")
check(n_docx + n_xlsx == 19, f"office骨架文件数=19 (实际 docx={n_docx}, xlsx={n_xlsx})")

# ---------- 2. 八项缺口产物锚点 ----------
S04 = os.path.join(BASE, "01_工作调研与课程标准/S04_课程标准/课程标准-{}.md".format(COURSE))
S06 = os.path.join(BASE, "03_学情与整体设计/S06_课程整体设计/课程整体设计-{}.md".format(COURSE))
S08 = os.path.join(BASE, "08_授课计划/授课计划-{}.md".format(COURSE))
S03ext = os.path.join(BASE, "01_工作调研与课程标准/S03_能力图谱与技能点（PGSD）/PGSD→学校图谱扩展映射表.md")
S07spec = os.path.join(BASE, "04_单元教学设计/S07单元设计骨架约定.md")
RUBRIC = os.path.join(BASE, "01_工作调研与课程标准/S04_课程标准/作品考核评分量规-{}.md".format(COURSE))
L1 = os.path.join(BASE, "09_S20模板缺口分析/course-code-baseline.md")

def has(path, *needles):
    try:
        t = open(path, encoding="utf-8").read()
    except Exception as e:
        return False, f"读取失败 {e}"
    miss = [n for n in needles if n not in t]
    return (len(miss) == 0), ("" if not miss else f"缺: {miss}")

for label, path, needles in [
    ("S04课标", S04, ["制定依据", "知识目标", "考核评价样表"]),
    ("S06整体设计", S06, ["附录 A：学校课程整体设计", "A.1 课程概况", "A.8 教学方法"]),
    ("S08授课计划", S08, ["思政要素", "纯作品考核", "教学时数按学期分配"]),
    ("S03扩展表", S03ext, ["布鲁姆", "技能难度", "思政点"]),
    ("S07骨架约定", S07spec, ["O1", "O2", "O3", "O4", "R1", "R10", "五步法"]),
    ("作品量规", RUBRIC, ["考核形式为作品", "试卷 A / B", "免笔试", "作品任务书"]),
    ("L1口径", L1, ["课程代码", "并存", "别名"]),
]:
    c, note = has(path, *needles)
    check(c, f"{label} 锚点: {note if note else 'OK'}")

# ---------- 3. S07 单元对齐区 + O代码一致 ----------
S07d = os.path.join(BASE, "04_单元教学设计")
weeks = sorted([f for f in os.listdir(S07d) if f.startswith("单元设计_第") and f.endswith(".md")]) if os.path.isdir(S07d) else []
check(len(weeks) >= 1, f"S07 单元文件存在 (实际 {len(weeks)})")
align = 0
o_map = {}
for f in weeks:
    t = open(os.path.join(S07d, f), encoding="utf-8").read()
    if "学校单元设计模板对齐速填区" in t:
        align += 1
    m = re.search(r"学习结果 O \| \*\*O(\d)\*\*", t)
    w = re.search(r"第(\d+)周", f)
    if m and w:
        o_map[int(w.group(1))] = int(m.group(1))
check(align == len(weeks), f"S07 含对齐区文件数={len(weeks)} (实际 {align})")
# O代码按周次规则: W1-2->O1, W3-11->O2, W12-14->O4（仅校验存在的周次）
exp = {w: (1 if w<=2 else 2 if w<=11 else 4) for w in o_map}
o_bad = [f"W{w}->O{o_map.get(w)}应为O{exp[w]}" for w in exp if o_map.get(w)!=exp[w]]
check(not o_bad, f"S07 O代码周次映射: {'OK' if not o_bad else '; '.join(o_bad)}")

# ---------- 4. S09 各周 R 索引 ----------
pack_root = os.path.join(BASE, "05_课堂备课包")
if os.path.isdir(pack_root):
    for d in sorted(os.listdir(pack_root)):
        if d.startswith("备课包_第") and os.path.isdir(os.path.join(pack_root, d)):
            p = os.path.join(pack_root, d, "资源R编码索引.md")
            c, note = has(p, "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10")
            check(c, f"S09 {d} R索引: {note if note else 'OK'}")

# ---------- 5. 基准一致性（课程名/学时/考核/禁特定证书体系） ----------
for label, path in [("S04", S04), ("S06", S06), ("S08", S08)]:
    if not os.path.exists(path):
        continue
    t = open(path, encoding="utf-8").read()
    check("特定证书体系" not in t, f"{label} 无'特定证书体系'禁用表述: {'OK' if '特定证书体系' not in t else '发现特定证书体系!'}")
    assess_ok = ("笔试" not in t) or any(k in t for k in ["免笔试", "不含笔试", "不补笔试题库", "纯作品"])
    check(assess_ok, f"{label} 考核口径(作品非笔试): {'OK' if assess_ok else '疑似笔试'}")

print("="*60)
print(f"通过项: {len(ok)}   问题项: {len(issues)}")
print("="*60)
if issues:
    print("【问题清单】")
    for i in issues:
        print("  x", i)
    print("\n>>> 存在未通过项，交付前 MUST 修复。")
else:
    print("✅ 全部核查通过，无问题。可交付/上传。")
print("-"*60)
print("通过项摘要:")
for o in ok:
    print("  ✓", o)
