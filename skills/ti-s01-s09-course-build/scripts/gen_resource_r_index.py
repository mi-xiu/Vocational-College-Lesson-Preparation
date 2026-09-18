#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# S09 备课包资源 → R1–R10 编码索引生成器（对齐 S07 骨架约定 §2.3）
# 动态发现 <base>/05_课堂备课包/ 下所有「备课包_第*」目录，按子目录映射生成 资源R编码索引.md。
# 用法：python3 scripts/gen_resource_r_index.py [--base /path/to/课程根] [--write]
import os, re, sys, argparse

parser = argparse.ArgumentParser(description="为 S09 各周备课包生成 资源R编码索引.md")
parser.add_argument("--base", default="/Users/a1-6/WorkBuddy")
parser.add_argument("--pack-root", default="05_课堂备课包")
parser.add_argument("--write", action="store_true", help="写文件；默认仅打印（dry）")
args = parser.parse_args()
BASE = args.base
PACK_ROOT = os.path.join(BASE, args.pack_root)

RULES = {
    "01_工作页": ("R4", "支架工具"),
    "02_考题": ("R9", "题库"),
    "03_量规": ("R3", "评价工具"),
    "04_学材": ("R1", "学习材料"),
    "05_讲稿": ("R1", "学习材料"),
    "06_PPT": ("R2", "技术工具"),
    "07_动画": ("R7", "动画"),
    "08_微课": ("R6", "微课"),
    "09_设备耗材安全": ("R2", "技术工具"),
    "10_拓展分层": ("R4", "支架工具"),
}
ENT_NAME = {"R1":"学习材料","R2":"技术工具","R3":"评价工具","R4":"支架工具",
            "R5":"企业资源","R6":"微课","R7":"动画","R8":"在线课程",
            "R9":"题库","R10":"反思互评"}

def classify(sub, base):
    if sub not in RULES:
        return None, None
    r, cat = RULES[sub]
    if sub == "03_量规" and "互评" in base:
        return "R10", "反思互评"
    if sub == "04_学材" and re.search(r"品牌手册|西溪爆款|版权素材|校企合作|岗位链|企业", base):
        return "R5", "企业资源"
    return r, cat

def collect(pack):
    root = os.path.join(PACK_ROOT, pack)
    items = {}
    for sub in os.listdir(root):
        sp = os.path.join(root, sub)
        if not os.path.isdir(sp):
            continue
        if sub == "00_本包说明":
            continue
        for fn in sorted(os.listdir(sp)):
            if fn.startswith("."):
                continue
            ext = os.path.splitext(fn)[1].lower()
            if ext not in (".md", ".docx", ".pptx"):
                continue
            base = os.path.splitext(fn)[0]
            if base.upper() == "README":
                continue
            r, cat = classify(sub, base)
            if r is None:
                continue
            key = (sub, base)
            if key not in items:
                items[key] = {"exts": set(), "sub": sub, "r": r, "cat": cat}
            items[key]["exts"].add(ext.lstrip("."))
    return items

def render(pack, items):
    wk = re.search(r"第(\d+)周", pack).group(1)
    theme = pack.split("_", 2)[-1] if len(pack.split("_")) > 2 else ""
    lines = []
    lines.append(f"# 资源 R 编码索引（第{wk}周·{theme}）\n")
    lines.append("> 对齐 `04_单元教学设计/S07单元设计骨架约定.md` §2.3 教学资源 R1–R10。\n")
    lines.append("> 本包现有资源按子目录归类映射；R8 在线课程本课程暂未单列，相关线上内容可并入 R6/R1。\n")
    lines.append("\n| 资源文件（去重 base） | 格式 | R 编码 | 类别 | 子目录 |")
    lines.append("|---|---|---|---|---|")
    counts = {f"R{i}": 0 for i in range(1, 11)}
    for (sub, base) in sorted(items.keys()):
        it = items[(sub, base)]
        exts = "/".join(sorted(it["exts"]))
        lines.append(f"| {base} | {exts} | {it['r']} | {it['cat']} | {sub} |")
        counts[it["r"]] += 1
    lines.append("\n## 编码汇总\n")
    for i in range(1, 11):
        r = f"R{i}"
        lines.append(f"- {r} {ENT_NAME[r]}：{counts[r]} 项")
    total = sum(counts.values())
    lines.append(f"\n> 合计 {total} 项资源已映射至 R1–R10。")
    return "\n".join(lines) + "\n"

WRITE = args.write
for pack in sorted(d for d in os.listdir(PACK_ROOT) if d.startswith("备课包_第") and os.path.isdir(os.path.join(PACK_ROOT, d))):
    items = collect(pack)
    out = render(pack, items)
    if WRITE:
        dst = os.path.join(PACK_ROOT, pack, "资源R编码索引.md")
        with open(dst, "w") as f:
            f.write(out)
        print(f"[WRITE] {pack}/资源R编码索引.md  ({len(items)} 资源)")
    else:
        print(f"\n========== DRY: {pack} ==========")
        print(out)
