# -*- coding: utf-8 -*-
"""build_course.py — 单课程三件套一键生成编排器（A/C/D 落地）

读 course.yaml（单一真源：身份 + 共享骨架） + 三套 spec（模板结构）
+ 各文档 data.json（长表单篇散文） → 叠加身份/骨架 → 渲染三件套 → 保真校验。

用法：
  python build_course.py <课程名> [--out 输出目录]

行为：
  - 身份字段（教师/代码/学校/专业…）与共享骨架（模块/周次/考核/评价）全部来自 course.yaml，
    改 course.yaml 一处即三文档同步更新（单一真源）。
  - 长表单篇散文（依据/目标/重难点/教学过程）在各 *-<课程>-data.json 中按文档独立维护。
  - 渲染后逐份跑 verify_faith（参数从 spec.verify 内嵌读取），全绿才算通过。
"""
import sys, os, json, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yaml
import render_template
import verify_faith

SPEC_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.dirname(SPEC_DIR)          # S04-学校模板
ROOT = os.path.dirname(TEMPLATE_DIR)              # 工作区根

# ---------- 文档定义：spec / data / 输出 / 身份 overlay / 骨架表 ----------
# overlay 的键 = 模板原文整段（旧文本），值 = 从 course.yaml identity 派生
# 这样"改 course.yaml 一处"即可让三文档身份同步（单一真源）

def make_docs(idt):
    return [
        {
            "name": "课程标准",
            "spec": "课程标准-模板-spec.json",
            "data": "课程标准-%s-data.json" % idt["course_name"],
            "out": "课程标准-%s.docx" % idt["course_name"],
            "overlay": {
                "西点装饰工艺": idt["course_name"],
                "酒店管理与数字化运营专业教研室 制": idt["office"],
                "课程代码：53338                                课程名称：西点装饰工艺": idt["code_line"],
                "课程类型：专业课                               学时/学分：68学时/4学分": idt["type_line"],
                "开课时间：第二学期                             适用专业：酒店管理与数字化运营": idt["semester_line"],
                "授课对象：酒店管理与数字化运营专业一年级学生": idt["object_line"],
            },
            "tables": None,  # 由骨架填充（见 build_tables）
            "kind": "kebiao",
        },
        {
            "name": "授课计划",
            "spec": "授课计划-模板-spec.json",
            "data": "授课计划-%s-data.json" % idt["course_name"],
            "out": "授课计划-%s.docx" % idt["course_name"],
            "overlay": {
                "浙江经贸职业技术学院": idt["school"],
                "2025—2026学年第二学期": idt["academic_year"],
                "课 程 名 称         西点装饰工艺": idt["name_line"],
                "专业、班级  酒店管理与数字化运营251、252": idt["major_class_line"],
                "任 课 教 师": idt["teacher_line"],
                "学      院         创意设计学院": idt["college_line"],
                "二〇二六年三月一日编制": idt["compile_line"],
            },
            "tables": None,
            "kind": "shouke",
        },
        {
            "name": "单元教案",
            "spec": "单元教案-模板-spec.json",
            "data": "单元教案-%s-data.json" % idt["course_name"],
            "out": "单元教案-%s.docx" % idt["course_name"],
            "overlay": {
                "《西点装饰工艺》教案": idt["jiaoan_title"],
                "专　　业：酒店管理与数字化运营": idt["major_line"],
                "授课教师： ": "授课教师：%s" % idt["teacher"],
                "2026年3月1日": idt["compile_date"],
                "课程名称：西点装饰工艺": idt["course_name_line"],
                "授课年级：酒店管理与数字化运营251、252": idt["grade_line"],
                "授课教师：孟铁鑫": "授课教师：%s" % idt["teacher"],
            },
            "tables": {},  # 纯段落，无表
            "kind": "danyuan",
        },
    ]


def build_tables(course, kind):
    """从 course.yaml 共享骨架生成各文档的 tables / cells / totals。"""
    if kind == "kebiao":
        mods = course["modules"]
        total_hours = sum(int(m[2]) for m in mods)
        return {
            "tables": {
                "0": mods,
                "1": course["module_content"],
                "2": course["assessment"],
                "3": course["evaluation"],
            },
            "totals": {"0": {"2": str(total_hours)}},
        }
    if kind == "shouke":
        return {
            "tables": {"1": course["weeks"]},
            "cells": course["shouke_cells"],
        }
    return {"tables": {}}


def build_course(course_name, out_dir=None):
    cfg = yaml.safe_load(open(os.path.join(SPEC_DIR, "course.yaml"), encoding="utf-8"))
    if course_name not in cfg.get("courses", {}):
        print("✗ 课程不存在：%s（可选：%s）" % (course_name, list(cfg.get("courses", {}).keys())))
        return False
    course = cfg["courses"][course_name]
    idt = course["identity"]
    out_dir = out_dir or ROOT
    docs = make_docs(idt)
    all_ok = True
    for d in docs:
        spec_path = os.path.join(SPEC_DIR, d["spec"])
        data_path = os.path.join(SPEC_DIR, d["data"])
        out_path = os.path.join(out_dir, d["out"])
        if not os.path.exists(data_path):
            print("  ⚠ 跳过 %s：缺少散文数据文件 %s" % (d["name"], d["data"]))
            continue
        # 1) 读 spec + 散文 data
        spec = json.load(open(spec_path, encoding="utf-8"))
        tpl = spec.get("source_file", "")
        if tpl and not os.path.isabs(tpl):
            cand = os.path.join(SPEC_DIR, tpl)
            if os.path.exists(cand):
                tpl = cand
            elif os.path.exists(os.path.join(SPEC_DIR, "..", tpl)):
                tpl = os.path.join(SPEC_DIR, "..", tpl)
        spec["source_file"] = tpl
        data = json.load(open(data_path, encoding="utf-8"))

        # 2) 叠加身份（单一真源）
        for k, v in d["overlay"].items():
            if k in data.get("paragraphs", {}):
                data["paragraphs"][k] = v

        # 3) 叠加共享骨架表
        sk = build_tables(course, d["kind"])
        data.setdefault("tables", {})
        for tk, tv in sk.get("tables", {}).items():
            data["tables"][tk] = tv
        if "totals" in sk:
            data["totals"] = sk["totals"]
        if "cells" in sk:
            data["cells_values"] = sk["cells"]

        # 4) 渲染（render 内部按 spec 结构填充）
        render_template.render(spec, data, out_path)
        print("  ✔ 渲染 %s → %s" % (d["name"], os.path.basename(out_path)))

        # 5) 保真校验（参数从 spec.verify 内嵌读取）
        rep = verify_faith.verify(
            tpl, out_path,
            old_texts=None, expects=None,
            spec_path=spec_path,
        )
        mark = "🟢" if rep["pass"] else "🔴"
        print("  %s %s 保真校验：%d 项" % (mark, d["name"], len(rep["checks"])))
        for name, ok, msg in rep["checks"]:
            if not ok:
                print("      ✗ %s — %s" % (name, msg))
                all_ok = False
    return all_ok


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python build_course.py <课程名> [--out 目录]")
        sys.exit(1)
    name = sys.argv[1]
    out = None
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]
    ok = build_course(name, out)
    print("\n" + ("🟢 全部通过 — 三件套已按 course.yaml 单一真源生成并保真" if ok else "🔴 存在校验未通过，见上"))
    sys.exit(0 if ok else 2)
