# -*- coding: utf-8 -*-
"""单元教案通道 · 通用运行器（模板导出专家 · Ti08）

把"单元教案导出逻辑"从项目脚本提升为技能级通用通道：
- 模板段落结构（索引 / 章节 / 关键字定位）由 unit-lesson-plan-fieldmap.json 描述（模板级，课程无关）
- 课程内容（每个单元的目标 / 重难点 / 过程等）由调用方以 unit 字典提供（项目级）
- 课程专属清扫替换（如 烘焙→短剧）由调用方以 sweep 列表提供（项目级）

单元数据字段（unit 字典，至少包含以下键）：
  identity : title / major / teacher1 / date / project / course / grade / teacher2 / hours / place
  sections : overview / suzhi[3] / nengli[3] / zhishi[3] / zhongdian[2] / nandian[2] / prep_t[3] / prep_s
  process  : process_header（如 "四、 教学过程设计（2学时，共90分钟）"）
             teaching[ ("section", 学时标题) | ("step", 环节名(加粗), 说明(正文)) , ... ]
  tail     : homework_p / homework_g / eval_p / eval_r / reflect / ext[4] / assignment

用法：
  from unit_channel import export_units, load_plan
  export_units("unit-lesson-plan-template.docx", load_plan(), UNITS, OUT_DIR, sweep=SWEEP)
详见 references/unit-lesson-plan-channel.md
"""
import sys, os, json
from docx import Document
from docx.oxml.ns import qn

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
from engine import (get_rpr, get_ppr, force_rpr, set_para_text, make_para,
                    make_para_mixed, delete_block_between, sweep_replace,
                    locate_by_keyword, locate_after_heading)

DEFAULT_PLAN_PATH = os.path.join(HERE, "unit-lesson-plan-fieldmap.json")


def load_plan(plan_path=None):
    with open(plan_path or DEFAULT_PLAN_PATH, encoding="utf-8") as f:
        return json.load(f)


def _set_idx(doc, idx, text):
    set_para_text(doc.paragraphs[idx], text)


def export_unit(template_path, plan, unit, out_path, sweep=None):
    """导出单个单元教案 docx（格式零改动，只换内容，新段 pPr+rPr 双继承）。"""
    doc = Document(template_path)
    rpr_bold = get_rpr(doc.paragraphs[plan["rpr"]["bold_idx"]])
    rpr_norm = get_rpr(doc.paragraphs[plan["rpr"]["norm_idx"]])
    ppr_norm = get_ppr(doc.paragraphs[plan["rpr"]["ppr_norm_idx"]])

    idn, sec, pb, kw = plan["identity"], plan["sections"], plan["process_block"], plan["keyword_locate"]

    # ---- 1) 身份段（均位于过程块之前，索引稳定） ----
    _set_idx(doc, idn["title_idx"], unit["title"])
    _set_idx(doc, idn["major_idx"], unit["major"])
    _set_idx(doc, idn["teacher1_idx"], unit["teacher1"])
    _set_idx(doc, idn["date_idx"], unit["date"])
    _set_idx(doc, idn["project_idx"], unit["project"])
    _set_idx(doc, idn["course_idx"], unit["course"])
    _set_idx(doc, idn["grade_idx"], unit["grade"])
    _set_idx(doc, idn["teacher2_idx"], unit["teacher2"])
    _set_idx(doc, idn["hours_idx"], unit["hours"])
    _set_idx(doc, idn["place_idx"], unit["place"])

    # ---- 2) 目标 / 重难点 / 准备（节标题强制粗体，正文逐条替换） ----
    _set_idx(doc, sec["overview_idx"], unit["overview"])
    for j, t in enumerate(unit["suzhi"]):
        _set_idx(doc, sec["suzhi"][j], t)
    for j, t in enumerate(unit["nengli"]):
        _set_idx(doc, sec["nengli"][j], t)
    for j, t in enumerate(unit["zhishi"]):
        _set_idx(doc, sec["zhishi"][j], t)

    _set_idx(doc, sec["zhongdian_head_idx"], sec["zhongdian_head_text"])
    force_rpr(doc.paragraphs[sec["zhongdian_head_idx"]], rpr_bold)
    for j, t in enumerate(unit["zhongdian"]):
        _set_idx(doc, sec["zhongdian"][j], t)
    for j, t in enumerate(unit["nandian"]):
        _set_idx(doc, sec["nandian"][j], t)

    _set_idx(doc, sec["prep_head_idx"], sec["prep_head_text"])
    force_rpr(doc.paragraphs[sec["prep_head_idx"]], rpr_bold)
    for j, t in enumerate(unit["prep_t"]):
        _set_idx(doc, sec["prep_t"][j], t)
    _set_idx(doc, sec["prep_s_idx"], unit["prep_s"])

    _set_idx(doc, sec["process_header_idx"], unit["process_header"])
    force_rpr(doc.paragraphs[sec["process_header_idx"]], rpr_bold)

    # ---- 3) 删除模板教学过程块（anchor 之后 → "五、"之前），再重建 ----
    delete_block_between(doc, pb["anchor_idx"], pb["end_marker"])

    anchor = doc.paragraphs[pb["anchor_idx"]]._element
    for item in unit["teaching"]:
        if item[0] == "section":
            np = make_para(item[1], rpr_bold, ppr_norm)
        else:
            np = make_para_mixed(item[1], item[2], rpr_bold, rpr_norm, ppr_norm)
        anchor.addnext(np)
        anchor = np

    # ---- 4) 课后任务 / 考核 / 反思 / 拓展 / 作业（关键字定位，抗索引漂移） ----
    p = locate_by_keyword(doc, kw["homework_p"])
    if p:
        set_para_text(p, unit["homework_p"])
    p = locate_by_keyword(doc, kw["homework_g"])
    if p:
        set_para_text(p, unit["homework_g"])
    p = locate_by_keyword(doc, kw["eval_p"])
    if p:
        set_para_text(p, unit["eval_p"])
    p = locate_by_keyword(doc, kw["eval_r"])
    if p:
        set_para_text(p, unit["eval_r"])
    p = locate_by_keyword(doc, kw["reflect"])
    if p:
        set_para_text(p, unit["reflect"])
    for k, ext in zip(kw["ext"], unit["ext"]):
        p = locate_by_keyword(doc, k)
        if p:
            set_para_text(p, ext)
    p = locate_after_heading(doc, kw["assignment_after_heading"])
    if p:
        set_para_text(p, unit["assignment"])

    # ---- 5) 课程换皮安全网 ----
    if sweep:
        sweep_replace(doc, sweep)

    doc.save(out_path)
    return out_path


def export_units(template_path, plan, units, out_dir, sweep=None, name_fmt="{uid}"):
    """批量导出：units = {uid: unit_dict}；name_fmt 控制输出文件名（{uid} 占位）。"""
    os.makedirs(out_dir, exist_ok=True)
    paths = {}
    for uid, unit in units.items():
        out_path = os.path.join(out_dir, f"AI短剧编剧-单元教案-{uid}.docx" if name_fmt == "{uid}" else name_fmt.format(uid=uid))
        paths[uid] = export_unit(template_path, plan, unit, out_path, sweep=sweep)
    return paths
