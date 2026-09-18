# -*- coding: utf-8 -*-
"""md_to_course.py — 内容专家 md → course.yaml 骨架适配器（专家团衔接）

把符合 EXPERT_INTEGRATION.md 契约的 markdown 课程骨架，
转为/合并进 _spec/course.yaml，供 build_course.py 渲染三件套。

用法：
  python md_to_course.py <课程名>-课程骨架.md [--merge] [--out course.yaml]

不带 --merge：仅打印将要写入的 yaml 片段（dry-run）。
带   --merge：合并写入 course.yaml 的 courses[课程名]（不破坏其它课程）。
"""
import sys, os, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yaml

FIELD_MAP = {
    "课程代码": "code",
    "课程类型": "type",
    "学时": "hours",
    "学分": "credits",
    "开课学期": "semester",
    "适用专业": "major",
    "授课对象": "grade",
    "任课教师": "teacher",
    "学院": "college",
    "教研室": "office",
    "学校": "school",
    "学年": "academic_year",
    "编制日期": "compile_date",
}


def parse_md(path):
    text = open(path, encoding="utf-8").read()
    lines = text.splitlines()
    course_name = None
    identity = {}
    modules, content, assessment, weeks, evaluation = [], [], [], [], []
    section = None
    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        if s.startswith("# 课程名：") or s.startswith("# 课程名:"):
            course_name = s.split("：", 1)[-1].split(":", 1)[-1].strip()
            continue
        if s.startswith("## "):
            section = s[3:].strip()
            continue
        if s.startswith("- "):
            # 身份字段：- 字段：值
            m = re.match(r"-\s*([^：:]+)[：:]\s*(.+)", s)
            if m and course_name is None:
                # 标题行可能没匹配到，兼容 "# 课程名：X" 已处理
                pass
            elif m:
                key, val = m.group(1).strip(), m.group(2).strip()
                if key in FIELD_MAP:
                    identity[FIELD_MAP[key]] = val
            continue
        if section and "|" in s:
            parts = [p.strip() for p in s.split("|")]
            if section.startswith("模块"):
                # N. name | hours
                if len(parts) >= 2:
                    name = re.sub(r"^\d+\.\s*", "", parts[0])
                    modules.append([str(len(modules) + 1), name, parts[1]])
            elif section.startswith("内容要求"):
                if len(parts) >= 4:
                    modules_name = re.sub(r"^\d+\.\s*", "", parts[0])
                    content.append([modules_name, parts[1], parts[2], parts[3]])
            elif section.startswith("考核组成"):
                if len(parts) >= 3:
                    assessment.append([parts[0], parts[1], parts[2]])
            elif section.startswith("周次进程"):
                if len(parts) >= 8:
                    seq = parts[0]
                    week = parts[1]
                    weeks.append([seq, week] + parts[2:8])
            elif section.startswith("评价样表"):
                if len(parts) >= 6:
                    evaluation.append([parts[0], parts[1], parts[2], parts[3], parts[4], parts[5]])
    return course_name, identity, modules, content, assessment, weeks, evaluation


def build_block(name, identity, modules, content, assessment, weeks, evaluation):
    hours = int(identity.get("hours", 0) or 0)
    # 由身份派生带固定宽度的整行（与 build_course.py overlay 键对应）
    idt = {
        "course_name": name,
        "code": identity.get("code", ""),
        "type": identity.get("type", ""),
        "hours": hours,
        "credits": int(identity.get("credits", 0) or 0),
        "hours_credits": "%s学时%s" % (hours, ("/%s学分" % identity["credits"]) if identity.get("credits") else ""),
        "semester": identity.get("semester", ""),
        "major": identity.get("major", ""),
        "grade": identity.get("grade", ""),
        "major_class": identity.get("major", ""),
        "teacher": identity.get("teacher", "滔滔"),
        "college": identity.get("college", ""),
        "office": identity.get("office", ""),
        "school": identity.get("school", ""),
        "academic_year": identity.get("academic_year", ""),
        "compile_date": identity.get("compile_date", ""),
        "standard_name": "《%s》课程标准" % name,
        "textbook": "自编讲义",
        "reference": "",
        "platform": "",
        "code_line": "课程代码：%s                                课程名称：%s" % (identity.get("code", ""), name),
        "type_line": "课程类型：%s                               学时/学分：%s" % (identity.get("type", ""), "%s学时%s" % (hours, ("/%s学分" % identity["credits"]) if identity.get("credits") else "")),
        "semester_line": "开课时间：%s                             适用专业：%s" % (identity.get("semester", ""), identity.get("major", "")),
        "object_line": "授课对象：%s" % identity.get("grade", ""),
        "name_line": "课 程 名 称         %s" % name,
        "major_class_line": "专业、班级  %s" % identity.get("major", ""),
        "teacher_line": "任 课 教 师        %s" % identity.get("teacher", "滔滔"),
        "college_line": "学      院         %s" % identity.get("college", ""),
        "compile_line": "%s编制" % identity.get("compile_date", ""),
        "major_line": "专　　业：%s" % identity.get("major", ""),
        "grade_line": "授课年级：%s" % identity.get("major", ""),
        "jiaoan_title": "《%s》教案" % name,
        "course_name_line": "课程名称：%s" % name,
    }
    block = {"identity": idt}
    if modules:
        block["modules"] = modules
    if content:
        block["module_content"] = content
    if assessment:
        block["assessment"] = assessment
    if weeks:
        block["weeks"] = weeks
    if evaluation:
        block["evaluation"] = evaluation
    # 授课计划表0 单元格（默认从学时派生）
    if hours:
        block["shouke_cells"] = {
            "t_total_a": str(hours), "t_total_b": str(hours),
            "t_done_a": "0", "t_done_b": "0",
            "t_left_a": str(hours), "t_left_b": str(hours),
            "t_weeks": "16", "t_wper": "4", "t_term": str(hours),
            "t_lec": str(hours // 2), "t_prac": str(hours // 2),
            "t_exp": "0", "t_rev": "0", "t_exam": "0", "t_quiz": "0", "t_inter": "0", "t_other": "0",
            "t_sub": str(hours),
            "std": "《%s》课程标准，%s" % (name, identity.get("academic_year", "")[:4] or "2026"),
            "book": "自编讲义", "ref": "",
            "note7": "由模块递进实施，理实一体。", "note8": "覆盖全流程实操训练。",
            "note9": " ", "note10": " ", "note11": " ", "note12": " ", "note13": " ", "note14": " ",
            "note15": "受节假日放假等因素影响，实际教学周数可能微调，总学时不变。",
            "note16": "受节假日放假等因素影响，实际教学周数可能微调。",
        }
    return block


def main():
    if len(sys.argv) < 2:
        print("用法: python md_to_course.py <骨架.md> [--merge] [--out course.yaml]")
        sys.exit(1)
    md = sys.argv[1]
    merge = "--merge" in sys.argv
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(os.path.dirname(os.path.abspath(__file__)), "course.yaml")
    name, identity, modules, content, assessment, weeks, evaluation = parse_md(md)
    if not name:
        print("✗ 未解析到课程名（请在 md 顶部写 '# 课程名：XXX'）")
        sys.exit(1)
    block = build_block(name, identity, modules, content, assessment, weeks, evaluation)
    print("解析课程：%s | 模块%d 内容%d 考核%d 周次%d 评价%d" % (
        name, len(modules), len(content), len(assessment), len(weeks), len(evaluation)))
    if not merge:
        print("\n--- 将写入 course.yaml 的片段（dry-run，加 --merge 实际写入）---")
        print(yaml.safe_dump({name: block}, allow_unicode=True, sort_keys=False, indent=2))
        return
    # 合并写入
    cfg = yaml.safe_load(open(out, encoding="utf-8")) if os.path.exists(out) else {"courses": {}}
    cfg.setdefault("courses", {})[name] = block
    cfg.setdefault("current_course", name)
    if "identity_defaults" not in cfg:
        cfg["identity_defaults"] = {"teacher": identity.get("teacher", "滔滔")}
    yaml.safe_dump(cfg, open(out, "w", encoding="utf-8"), allow_unicode=True, sort_keys=False, indent=2)
    print("✔ 已合并写入 %s（courses.%s）" % (out, name))


if __name__ == "__main__":
    main()
