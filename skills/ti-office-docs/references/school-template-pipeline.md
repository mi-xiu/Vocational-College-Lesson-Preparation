# 学校官方模板保真管线（S04 学校模板）· 工作指南

> 适用：课程需落入**学校官方 Word 模板**（课程标准 / 授课计划 / 单元教案等）做交付，要求成品与模板"肉眼一致"。

## 0. 铁律

**先 optimize 再 render。** 任何类似学校模板，禁止每门课现场重写 Python 探查模板；一律先跑优化器产出 enriched 规格卡（一次性、永久复用），再做渲染执行。新课件只改数据文件，跑一次即出 docx。

---

## 1. 项目布局约定

把以下文件放在**同一个课程项目目录**（如 `S04-学校模板/`）：

```
<项目>/
├── course-standard-template.docx           # 学校官方模板（源，永不改）
├── teaching-plan-template.docx
├── unit-lesson-plan-template.docx
├── _spec/                       # 管线工作区
│   ├── optimize_template.py     # 优化器
│   ├── render_template.py       # 渲染器
│   ├── verify_faith.py          # 保真校验器
│   ├── build_course.py          # 单课编排器（参考实现）
│   ├── md_to_course.py          # 内容专家契约 → course.yaml
│   ├── course.yaml              # 单一真源（身份 + 共享骨架）
│   ├── 课程标准-<课程>-data.json # 长表单篇散文（按文档）
│   ├── 授课计划-<课程>-data.json
│   ├── 单元教案-<课程>-data.json
│   └── *-spec.json              # 优化器产出的 enriched 规格卡
```

`scripts/school-template/` 下的 5 个 .py 与 `references/spec-examples/` 下的 3 套 spec 即本技能自带副本，复制到项目 `_spec/` 即可用。

---

## 2. 三步工作流

### 阶段 A · 优化（每模板一次性）
```bash
python optimize_template.py course-standard-template.docx   # → course-standard-template-spec.json
python optimize_template.py teaching-plan-template.docx   # → teaching-plan-template-spec.json
python optimize_template.py unit-lesson-plan-template.docx   # → unit-lesson-plan-template-spec.json
```
产出 `*-spec.json`：段落整段 match 键、表格 `mode`（fill/rebuild/cells）+ `merge_cols` + `col_widths` + 表头 + 合计行，并内嵌 `verify` 段（forbidden/expect）与 `rules` 段（校正规则）。

### 阶段 B · 准备数据与单一真源
- `course.yaml` 写 `courses.<名>` 块：`identity`（教师/代码/学校/专业…）+ `modules`/`weeks`/`assessment`/`evaluation`（共享骨架）。
- 各文档 `*-<课程>-data.json`：段落散文 + 表数据。
- 内容来自专家团时：先由内容专家出**契约 md**，再 `python md_to_course.py 契约.md` → 生成 `course.yaml` 骨架（见 `EXPERT_INTEGRATION.md`）。

### 阶段 C · 渲染 + 校验（每课）
```bash
python build_course.py <课程名>          # 读 course.yaml + spec + data → 渲染三件套 → 逐份 verify
```
`build_course.py` 自动：①叠加身份（单一真源）②叠加共享骨架表 ③渲染 ④跑 `verify_faith`（`spec.verify` 参数内嵌）→ 全绿才算通过。

> 单文档手渲：`python render_template.py <spec.json> <data.json> <out.docx>`，再 `python verify_faith.py <模板.docx> <out.docx> --spec <spec.json>`。

---

## 3. 保真校验（替代人工抽表）

`verify_faith.py` 两级：
- **结构级**：表头/合计/数据行签名子集、段落样式字体、占位符残留、旧文本残留。
- **内容级**：`--expect` 关键字段存在；自动校验配分列/比例列合计 = 100；比例列精确表头匹配（避免误命中"成绩组成及比例"子串）。

一次跑通即绿灯。

---

## 4. 校正规则库（python-docx 坑，已固化）

见 `SPEC_RULES.md`。要点：
- **vMerge**：纵向合并时 `row.cells[ci]` 对所有行返回同一合并 cell 对象 → 重建表按 `merge_cols` 直写 vMerge。
- **fill 合计行**：模板末行即合计行（非 hr+len），填完删多余行。
- **段落匹配**：全文精确匹配最稳；模板尾随空格 → `rstrip()` 回退。
- **多段单元格**：`setc` 填值前清除多余段落，否则旧文本残留。
- **仅合计行含合并的表**（如成绩组成表）保留原生合并走 fill，勿误判 rebuild。

---

## 5. 专家团衔接

office-docs 是专家团文档统一出口。内容专家（course-standard / blueprint / unit-design）出**契约 md** → `md_to_course.py` 转 `course.yaml` → `build_course.py` 出 docx。契约格式见 `EXPERT_INTEGRATION.md`。

---

## 6. 版本

本管线随 `ti-office-docs` 技能 v1.1.0 并入 `gzv-office-docs` 专家（包 v1.3.1）与 `vocational-college-lesson-preparation` 专家团（包 v1.3.1）。
