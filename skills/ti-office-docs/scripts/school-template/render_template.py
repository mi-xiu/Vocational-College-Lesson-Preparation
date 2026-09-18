# -*- coding: utf-8 -*-
"""通用模板渲染器：读 规格json + 数据json -> 生成保真 docx。

支持四种填充模式（由规格 render 段声明）：
  paragraphs : 段落整段替换（精确/包含）
  fill       : 表格逐行填充 + 截断多余行 + 可选合计行（保留表头合并）
  rebuild    : 按合并列重建表格（干净填充，匹配模板纵向合并签名）
  cells      : 指定单元格坐标填值（适合结构固定、仅改数值的复杂合并表）

用法：
  python render_template.py <spec.json> <data.json> <out.docx>
"""
import sys, json, os
from copy import deepcopy
from docx import Document
from docx.oxml.ns import qn

# ---------- 保真底层函数（沿用已验证实现）----------
def replace_in_para(p, old, new):
    full = "".join(r.text for r in p.runs) if p.runs else p.text
    if old not in full:
        return False
    new_full = full.replace(old, new)
    if p.runs:
        p.runs[0].text = new_full
        for r in p.runs[1:]:
            r._element.getparent().remove(r._element)
    else:
        p.text = new_full
    return True

def replace_all(doc, old, new):
    for p in doc.paragraphs:
        if old in ("".join(r.text for r in p.runs) if p.runs else p.text):
            replace_in_para(p, old, new)

def setc(cell, text):
    # 清掉模板单元格中可能存在的多余段落（避免旧文本残留在后续段落）
    paras = cell.paragraphs
    for p in paras[1:]:
        p._element.getparent().remove(p._element)
    para = cell.paragraphs[0]
    if para.runs:
        para.runs[0].text = text
        for r in para.runs[1:]:
            r._element.getparent().remove(r._element)
    else:
        para.text = text

def del_row_range(tbl, start, end):
    for i in range(end, start - 1, -1):
        if i < len(tbl.rows):
            tr = tbl.rows[i]._tr
            tr.getparent().remove(tr)

def get_col_widths(tbl):
    row = tbl.rows[1] if len(tbl.rows) > 1 else tbl.rows[0]
    ws = []
    for c in row.cells:
        tcPr = c._tc.find(qn('w:tcPr'))
        w = ""
        if tcPr is not None:
            we = tcPr.find(qn('w:tcW'))
            if we is not None:
                w = we.get(qn('w:w'))
        ws.append(w)
    return ws

def get_body_rpr(tbl):
    for r in tbl.rows[1].cells[0].paragraphs[0].runs:
        return deepcopy(r._element.find(qn('w:rPr')))
    return None

def set_cell_vmerge_restart(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    for e in tcPr.findall(qn('w:vMerge')):
        tcPr.remove(e)
    v = tcPr.makeelement(qn('w:vMerge'), {qn('w:val'): 'restart'})
    tcPr.append(v)

def _apply_width(cell, w):
    if not w:
        return
    tcPr = cell._tc.get_or_add_tcPr()
    we = tcPr.find(qn('w:tcW'))
    if we is None:
        we = tcPr.makeelement(qn('w:tcW'), {})
        tcPr.append(we)
    we.set(qn('w:w'), w)
    we.set(qn('w:type'), 'dxa')

def _apply_rpr(cell, rpr):
    para = cell.paragraphs[0]
    if not para.runs:
        return
    run = para.runs[0]
    dst = run._element.get_or_add_rPr()
    for child in list(dst):
        dst.remove(child)
    for child in rpr:
        dst.append(deepcopy(child))

def rebuild_table(doc, idx, header, rows, widths, merge_cols, body_rpr, header_rows=1, totals=None):
    """按合并列重建表格——保留原表头行(含跨列合并)与列宽，数据行以模板首个数据行为样式模板
    (清除其 vMerge/gridSpan 使成独立行) 逐行追加并填文本，实现"内容变、格式零漂移"。
    totals: {列索引: 文本} 用于填充被保留的合计/小计行。
    """
    old = doc.tables[idx]
    ncols = len(header)
    # 检测并保留合计/小计行
    has_total = False
    total_tr = None
    if len(old.rows) > header_rows:
        last_text = " ".join(c.text for c in old.rows[-1].cells)
        if "合计" in last_text or "小计" in last_text:
            has_total = True
            total_tr = deepcopy(old.rows[-1]._tr)
    # 抓首个数据行作样式模板
    tmpl_tr = None
    if len(old.rows) > header_rows + (1 if has_total else 0):
        tmpl_tr = deepcopy(old.rows[header_rows]._tr)
    tbl_el = old._tbl
    # 删除表头之后的所有行（数据行 + 合计行）
    for i in range(len(old.rows) - 1, header_rows - 1, -1):
        tbl_el.remove(old.rows[i]._tr)
    if tmpl_tr is None:
        return
    # 清除模板数据行的纵向合并/跨列合并，保留列宽与字体，形成"独立行模板"
    for tc in tmpl_tr.findall(qn('w:tc')):
        tcPr = tc.find(qn('w:tcPr'))
        if tcPr is not None:
            for tag in (qn('w:vMerge'), qn('w:gridSpan')):
                for e in tcPr.findall(tag):
                    tcPr.remove(e)
    # 追加数据行并填文本
    for rdata in rows:
        tbl_el.append(deepcopy(tmpl_tr))
    for ri, rdata in enumerate(rows):
        row_obj = old.rows[header_rows + ri]
        for ci, val in enumerate(rdata):
            if ci < len(row_obj.cells):
                setc(row_obj.cells[ci], val)
    # 追加合计行并填合计值
    if has_total and total_tr is not None:
        tbl_el.append(total_tr)
        if totals:
            trow = old.rows[-1]
            for col, txt in totals.items():
                if int(col) < len(trow.cells):
                    setc(trow.cells[int(col)], txt)

# ---------- 渲染主逻辑 ----------
def render(spec, data, out_path):
    tpl = spec["source_file"]
    doc = Document(tpl)
    rt = spec.get("render", {})

    # 1) 段落：按"实际文档段落全文"在 data.paragraphs 中精确匹配替换
    #    （data.paragraphs 的键 = 模板原文整段文本，值 = 新文本；匹配稳健，不依赖索引顺序）
    pdata = data.get("paragraphs", {})
    for p in doc.paragraphs:
        cur = "".join(r.text for r in p.runs) if p.runs else p.text
        # 精确匹配优先；模板段落常带尾随空白，回退到 rstrip 匹配
        key = cur if cur in pdata else (cur.rstrip() if cur.rstrip() in pdata else None)
        if key is not None:
            replace_in_para(p, cur, pdata[key])

    # 2) 表格
    for te in rt.get("tables", []):
        idx = te["idx"]
        mode = te.get("mode", "fill")
        key = str(idx)
        tbl = doc.tables[idx]
        if mode == "fill":
            rows_data = data.get("tables", {}).get(key, [])
            hr = te.get("header_rows", 1)
            for i, row in enumerate(rows_data):
                if hr + i >= len(tbl.rows):
                    break
                tr = tbl.rows[hr + i]
                for ci, val in enumerate(row):
                    if ci < len(tr.cells):
                        setc(tr.cells[ci], val)
            # 合计行：模板末行为合计（即使本课程的模块数少于模板，合计仍在最后一行）
            if te.get("total"):
                trow = tbl.rows[-1]
                for col, txt in te.get("total_label", {}).items():
                    setc(trow.cells[int(col)], txt)
                for col, txt in data.get("totals", {}).get(key, {}).items():
                    setc(trow.cells[int(col)], txt)
                del_start = hr + len(rows_data)
                del_end = len(tbl.rows) - 2  # 保留 表头 + 数据 + 末行(合计)
            else:
                del_start = hr + len(rows_data)
                del_end = len(tbl.rows) - 1
            if del_start <= del_end:
                del_row_range(tbl, del_start, del_end)
        elif mode == "rebuild":
            rows_data = data.get("tables", {}).get(key, [])
            rebuild_table(doc, idx, te["header"], rows_data,
                          te.get("col_widths", get_col_widths(tbl)),
                          te.get("merge_cols", []), get_body_rpr(tbl),
                          te.get("header_rows", 1),
                          data.get("totals", {}).get(key, {}))
        elif mode == "cells":
            vals = data.get("cells_values", {})
            for cs in te.get("cells", []):
                r, c, k = cs["r"], cs["c"], cs["k"]
                if k in vals and r < len(tbl.rows) and c < len(tbl.rows[r].cells):
                    setc(tbl.rows[r].cells[c], vals[k])

    # 3) 全局清扫（课程特定旧标记）
    for old, new in data.get("sweep", []):
        replace_all(doc, old, new)

    doc.save(out_path)
    return doc

if __name__ == "__main__":
    spec_path, data_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    with open(spec_path, encoding="utf-8") as f:
        spec = json.load(f)
    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)
    # source_file 解析：依次尝试 直接路径 / 规格同目录 / 规格上级目录
    tpl = spec.get("source_file", "")
    if tpl and not os.path.isabs(tpl):
        d = os.path.dirname(os.path.abspath(spec_path))
        for cand in (tpl, os.path.join(d, tpl), os.path.join(d, "..", tpl)):
            if os.path.exists(cand):
                tpl = cand
                break
    spec["source_file"] = tpl
    render(spec, data, out_path)
    print("SAVED:", out_path)
