# 单元教案通道（Ti08 模板导出专家 · 通用导出通道）

> 把"单元教案导出逻辑"从单课程项目脚本（`99_工程与脚本/export_unit.py`）提升为**技能级通用通道**，
> 与任何具体课程解耦：**模板级结构**在技能内（`unit-lesson-plan-fieldmap.json`），**课程内容**由调用方提供，
> **课程专属换皮**由调用方以 sweep 列表提供。新增课程只需提供内容，无需重写导出脚本。

---

## 1. 架构（三件套）

| 文件 | 角色 | 是否绑定课程 |
|---|---|---|
| `scripts/unit-lesson-plan/engine.py` | 通用段落引擎原语（pPr+rPr 双继承、删块、清扫、定位） | 否 |
| `scripts/unit-lesson-plan/unit_channel.py` | 通用运行器 `export_unit / export_units` | 否 |
| `scripts/unit-lesson-plan/unit-lesson-plan-fieldmap.json` | 默认单元教案模板的段落映射（索引/章节/关键字定位） | 模板级（否） |
| `references/template-field-mapping.md` | 模板字段 ↔ 项目来源 总映射 | 否 |
| 调用方项目脚本（如 `export_unit.py`） | 课程内容 `UNITS` + 身份段 + sweep 列表 | **是** |

> 关键分离：**模板怎么排**（fieldmap）归技能；**教什么**（unit 数据）归课程；
> **旧模板换皮**（sweep）归课程。三者正交，新增课程 = 复制 fieldmap + 写 unit 数据。

---

## 2. 数据契约（unit 字典必填字段）

```python
unit = {
  # 身份段（模板头部）
  "title": "《XX》教案", "major": "专　　业：…", "teacher1": "授课教师：【待填】",
  "date": "2026年8月20日", "project": "项目X：…", "course": "课程名称：…",
  "grade": "授课年级：…", "teacher2": "授课教师：【待填】",
  "hours": "课时安排：2课时", "place": "授课地点：…",
  # 正文段
  "overview": "本教学单元…",
  "suzhi":   ["1）…", "2）…", "3）…"],      # 素质目标 3 条
  "nengli":  ["1）…", "2）…", "3）…"],      # 能力目标 3 条
  "zhishi":  ["1）…", "2）…", "3）…"],      # 知识目标 3 条
  "zhongdian": ["1、…", "2、…"],            # 教学重点 2 条
  "nandian":   ["1、…", "2、…"],            # 教学难点 2 条
  "prep_t":  ["多媒体课件：…", "…", "…"],    # 教师准备 3 条
  "prep_s":  "预习…",                        # 学生准备
  "process_header": "四、 教学过程设计（2学时，共90分钟）",
  "teaching": [                              # 教学过程（BOtPPPS）
      ("section", "第1学时（45分钟）：…"),
      ("step", "1、Bridge-in 导入（8分钟）：", "播放…"),
      ("step", "2、Objective 目标（4分钟）：", "明示…"),
      # … 更多 step …
      ("section", "第2学时（45分钟）：…"),
      ("step", "N、环节名（X分钟）：", "说明…"),
  ],
  # 尾部段
  "homework_p": "个人作业：…", "homework_g": "小组预习：…",
  "eval_p": "过程性评价（60%）：…", "eval_r": "成果性评价（40%）：…",
  "reflect": "关注学生是否…",
  "ext": ["微课：…", "动画：…", "在线课程：…", "案例库：…"],
  "assignment": "完善…",
}
```

`teaching` 项两种形态：
- `("section", 学时标题)` → 整段粗体（节标题 rPr + 正文 pPr）
- `("step", 环节名(加粗), 说明(正文))` → 前缀粗体 + 正文常规，整段继承 pPr

---

## 3. 调用方式

```python
import sys, os
BASE = r".../skills/ti-office-docs"
sys.path.insert(0, BASE + "/scripts/unit-lesson-plan")
import unit_channel as UC

UNITS = { "U1": {...}, "U2": {...} }          # 课程内容（项目级）
IDENTITY = { "title": "《XX》教案", ... }      # 课程身份段（项目级）
SWEEP = [("旧模板词", "新课程词"), ...]        # 课程换皮（项目级）

for uid, u in UNITS.items():
    unit = dict(u); unit.update(IDENTITY); unit["process_header"] = "四、 教学过程设计（2学时，共90分钟）"
    UC.export_unit(f"{BASE}/templates/unit-lesson-plan-template.docx", UC.load_plan(), unit,
                   f"word版/XX-单元教案-{uid}.docx", sweep=SWEEP)
```

`UC.load_plan()` 默认读取同目录 `unit-lesson-plan-fieldmap.json`（默认模板映射）。换用其他单元教案模板时，
可传入自定义 fieldmap 路径（字段结构一致即可复用引擎）。

---

## 4. S07 → Ux 路由触发（单元设计 → 单元教案）

**触发条件**：当 **S07 单元设计专家（Ti06）** 产出 `单元设计.md`（含 U1–U8 各单元的目标/重难点/准备/教学过程/考核/反思）
且用户要求"输出可上课的单元教案 docx"或"按学校/默认单元教案模板导出"时，

**路由动作**：
1. 主理人（Ti00）或用户把每个单元 Ux 派发给 **Ti08 模板导出专家**；
2. Ti08 加载 `ti-office-docs` → 单元教案通道：把 Ux 的单元设计内容映射为上述 unit 字典；
3. 调用 `export_unit(...)` 生成 `XX-单元教案-Ux.docx`（格式零改动，只换内容）；
4. 逐份 `verify_faith.py` 保真校验（段落[样式+字体] 子集 + 占位符/旧文本残留）→ 全绿交付。

**边界（红线）**：
- 单元教案通道只做"格式套用"，**不重写教学逻辑**；教学科学性以 S07 单元设计母本为准。
- 若 S07 单元数/学时与默认模板（样例为 4 学时）不同，属正常——`verify_faith` 已改为"签名子集"判定，
  只校验格式不引入新样式，不卡段落数量。
- 模板未过"规范化门"不得进入生成（见 SKILL.md 第 0 步）。

---

## 5. 关键纪律（已固化）

> **新插入段落必须同时继承 pPr + rPr**。
> 内容重写（如教学过程块删除重建）时，若只复制 run 的 `rPr`（字体），会丢失段落 `pPr`
> （首行缩进 `ind firstLineChars`、行距 `spacing line`），导致新段回退为无缩进/默认行距。
> 引擎在 `make_para / make_para_mixed` 中强制同时复制 pPr（本项目模板：`firstLineChars=200`
> 首行缩进 2 字符 + `line=360/auto` 1.5 倍行距），从根源杜绝该缺陷。
