# 职教课程开发专家团 · 分享操作指引

> 适用版本：WorkBuddy 当前桌面版（专家/专家团注册于 `my-experts` marketplace）
> 当前打包状态：`gzv-office-docs` 与 `vocational-college-lesson-preparation` = **v1.3.1**；其余 9 个独立专家包 = v1.3.0
> 配套文档：《VERSIONING.md》（已随团队包分发）

---

## 〇、铁律：先备份，再分享

GUI 一键分享会把**你本地源包**清成残壳（`.codebuddy-plugin/` 空、`skills/` 缺目录、`plugin.json` 丢失，甚至 `gzv-*` 独立包被移除）。分享出去的内容是完整的，但你自己的源坏了。

**因此任何分享/打包动作前，先备份：**

- 已为你备好：`_backup/vocational-college-lesson-preparation-v1.3.1-<时间戳>.zip`（含全部 10 个独立包 + 团队包 + `marketplace.json` 注册表 + 版本清单）
- 还原方法：把备份里 `plugins/*` 与 `.codebuddy-plugin/marketplace.json` 覆盖回 `~/.workbuddy/plugins/marketplaces/my-experts/` 对应位置即可。

> 离线 `.wbp` 打包（方法二）**不会**破坏本地源，但仍建议先备份以防误操作。

---

## 一、方法一：GUI 一键分享（在线）

### 标准点击路径
1. 打开 **专家中心**：左侧边栏点「**专家**」（或「专家·技能·连接器」入口）。
2. 切到 **「我的专家」** 标签页（你自己注册/创建的才在这里；官方精选在「专家广场」，**广场里的卡片没有分享按钮**，要在「我的专家」找）。
3. 找到目标卡片：
   - 单个专家：如「Ti08 Office 文档专家（v1.3.1）」
   - 专家团：如「职教课程开发专家团（v1.3.1）」
4. 在卡片上找 **分享入口**（三种可能，按你的界面版本看哪种出现）：
   - **A. 卡片悬停**：鼠标移到卡片上，右上角/底部浮现操作条，含「分享」图标（常是 ↗ 或 分享 文字）；
   - **B. 卡片「⋯」菜单**：卡片角落有「⋯」（更多）按钮，点开里面有「分享」；
   - **C. 详情页**：点进卡片进入专家详情/对话页，在**右上角**或页内找「分享」按钮。
5. 点「分享」→ 自动生成 **分享链接 / 二维码** → 发给好友，对方打开即一键添加。

### 找不到分享按钮的排查（你遇到的问题）
- ✅ 确认在 **「我的专家」** 而非「专家广场」——广场卡片不可分享。
- ✅ 确认卡片是 **你自己注册**的（本团队已 `register_expert.py` 注册进 `my-experts`，应出现在「我的专家」）。
- ✅ 试着 **把鼠标悬停在卡片上**、或点开卡片 **「⋯」菜单**、或 **进入详情页看右上角**——分享入口常藏在三处之一。
- ✅ 检查 WorkBuddy 是否为**较新版本**；极旧版本可能未上线分享功能，建议升级客户端。
- ⚠️ 若以上都无解：直接走 **方法二（.wbp 离线打包）**，这是 100% 可控、不依赖 GUI 的路径，且我已帮你打好（见第四节）。

> 说明：我作为运行在 WorkBuddy 内的 AI，**无法直接操控桌面客户端去点击按钮**。分享按钮是界面元素，只能由你在客户端手动点；我能做的是给你精确路径，或用脚本直接产出可分发的安装包。

---

## 二、方法二：`.wbp` 离线打包（推荐，可控）

### 已为你打好的包（当前版本 v1.3.1）
位于工作区 `专家团分享包/`：
- `vocational-college-lesson-preparation.wbp`（6.2 MB）—— **整团一个包**，内部已嵌入全部 10 位专家副本，双击即装整团。
- `gzv-office-docs.wbp`（1.6 MB）—— 仅 Office 文档专家独立包（本次管线升级的载体）。

### 自己重新打包（如需）
官方打包脚本（先 `validate` 再 `zip`）：
```bash
python3 ~/.workbuddy/plugins/cache/workbuddy-builtin/skill-expert-manager/0.1.0/scripts/package_expert.py \
  ~/.workbuddy/plugins/marketplaces/my-experts/plugins/vocational-college-lesson-preparation \
  ~/Desktop/
```
- 输出 `<名>.zip`，双击安装时 WorkBuddy 接受 zip 改名 `.wbp`（本质都是 zip）。
- 团队包会一并打包其内嵌的 `skills/` 副本，无需单独打每个成员。

### 接收方安装
- **Mac/Windows**：双击 `.wbp`（或 `.zip`）→ WorkBuddy 自动识别并安装到「我的专家」。
- 离线、无需联网、无需对方有账号。

---

## 三、分发策略速查

| 场景 | 推荐做法 |
|---|---|
| 给同平台好友在线装 | 方法一「我的专家」卡片分享（**先备份**，分享后如本地源损坏用备份还原） |
| 批量给同事 / 换机 / 离线 | 直接发 `专家团分享包/vocational-college-lesson-preparation.wbp`（最稳） |
| 只要单个专家 | 发对应 `gzv-*.wbp`（如 `gzv-office-docs.wbp`） |
| 整机重装 / 最完整还原 | 用 `专家团统一安装包_*.zip` + `安装专家团.command`（Mac 双击即装） |

---

## 四、版本纪律（分发前核对）

- 团队包与 office-docs 已升 **v1.3.1**（本次补丁：并入 S04 学校模板保真管线）。
- 其余 9 个独立专家包保持 **v1.3.0**（本次未改动，合法）。
- 分发文件名建议保留 `vX.Y.Z` 标识，便于接收方核对版本。
- 版本号规则详见团队包内《VERSIONING.md》：仅局部改动 → `Z+1`（本次即此）；全体统一发版 → `Y+1`；破坏性变更 → `X+1`。

---

## 五、恢复（万一本地源被 GUI 分享清空）

1. 解压 `_backup/vocational-college-lesson-preparation-v1.3.1-<时间戳>.zip`。
2. 把其中 `plugins/` 下全部目录覆盖回 `~/.workbuddy/plugins/marketplaces/my-experts/plugins/`。
3. 把 `.codebuddy-plugin/marketplace.json` 覆盖回 `~/.workbuddy/plugins/marketplaces/my-experts/.codebuddy-plugin/marketplace.json`。
4. 重启 WorkBuddy，专家团恢复如初。
