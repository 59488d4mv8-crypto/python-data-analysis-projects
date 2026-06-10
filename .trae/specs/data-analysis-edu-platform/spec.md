# 商务数据分析在线教育平台 - Product Requirement Document

## Overview
- **Summary**: 一款面向商务数据分析与应用专业学生的在线学习平台，提供完整的课程体系、互动式 Python 数据分析学习模块、练习与测评功能，以及成就激励系统。平台以静态网站形式部署于 Cloudflare Pages，通过 Pyodide 在浏览器端原生运行 Python 代码，无需独立后端服务器。
- **Purpose**: 为商务数据分析专业学生提供一站式、低门槛、高互动的 Python 数据分析学习体验，解决传统学习中"看了不会写、写了跑不起来、缺乏即时反馈"的痛点。
- **Target Users**: 商务数据分析与应用专业的高职/本科学生、相关专业教师、对数据分析感兴趣的自学者。

## Goals
- 提供系统化、模块化的商务数据分析课程，覆盖从 Python 基础到高级数据分析方法
- 实现浏览器端 Python 代码的实时编写与运行（基于 Pyodide），无需本地环境
- 构建学-练-测评闭环，每个知识点配套讲解、互动练习与阶段性测评
- 设计成就激励系统（积分、徽章、等级、学习时长统计），提升学习动力
- 以纯静态站点方式部署至 Cloudflare Pages，在免费方案内稳定运行

## Non-Goals (Out of Scope)
- **不提供**服务器端 Python 运行环境（所有 Python 代码在学生浏览器内执行）
- **不实现**多用户云端同步与社交功能（学习数据本地存储，课程发布后不依赖后端）
- **不做**视频流/直播授课，课程以图文 + 代码互动形式呈现
- **不支持**大规模并发考试与自动阅卷（测评以浏览器端即时判分为主）
- **不包含**支付/订阅系统，平台免费使用
- **不实现**教师后台与课程在线编辑 CMS（课程内容以 Markdown/JSON 形式在构建阶段打包）

## Background & Context
- **Cloudflare Pages 免费方案限制**：每次构建 ≤1 分钟、每月 500 次构建、带宽 100GB/月、Pages Functions 仅支持 JS/TS（Workers 运行时）、**无原生 Python 后端支持**
- **Python 执行方案选择**：采用 [Pyodide](https://pyodide.org/) 基于 WebAssembly 在浏览器端运行 CPython，支持 numpy、pandas、matplotlib、scipy、scikit-learn 等主流数据分析库，完美契合本项目教学需求
- **数据持久化方案**：用户学习进度、积分、徽章通过浏览器 `localStorage` 存储；无需后端数据库，不产生服务器成本
- **前端框架**：采用轻量级静态站点生成器（纯 HTML/CSS/JS 或 Astro/Vite 静态构建），确保构建快、体积小，符合 Cloudflare Pages 免费方案资源限制
- **课程内容**：以 Markdown/JSON 文件组织，构建阶段打包为静态资源；支持增量更新

## Functional Requirements
- **FR-1 课程体系**：平台提供至少 6 个模块化课程单元，涵盖 Python 基础、NumPy、Pandas、数据可视化、统计分析、商业案例实战；每个单元包含若干章节，每章节含学习目标、知识讲解、代码示例、练习与小结
- **FR-2 导航与学习路径**：首页展示课程列表与学习进度；用户可按顺序学习或自由跳转；左侧目录树显示章节结构与完成状态
- **FR-3 互动代码编辑器**：每个学习模块嵌入代码编辑器（基于 CodeMirror 或 Monaco Editor 轻量版），支持：① 预置示例代码；② 学生自由编辑；③ 点击"运行"在浏览器端通过 Pyodide 执行 Python；④ 控制台输出实时展示；⑤ matplotlib 图表在页面内渲染
- **FR-4 练习系统**：每章节配备 2-5 道编程练习；练习给出任务描述与初始代码；学生完成后点击"检查答案"，系统通过预设测试用例（Pyodide 执行断言）判断正确性并即时反馈
- **FR-5 测评系统**：每单元结束提供单元测评（含选择题 + 编程题）；选择题即时判分；编程题通过测试用例判分；测评结束显示得分与薄弱知识点提示；测评成绩记入总分
- **FR-6 成就激励系统**：① 积分：完成章节+10、练习全对+20、测评≥80分+50；② 徽章：完成首章、首个满分练习、首个测评通关、连续学习 7 天、累计学习 10 小时、完成全部课程等；③ 等级：积分累计升级（Lv.1~Lv.10），每级有积分阈值；④ 学习统计：学习时长、完成章节数、正确率曲线
- **FR-7 学习数据持久化**：所有学习进度、积分、徽章、测评成绩自动保存至 localStorage；支持"导出学习数据 JSON"和"导入学习数据 JSON"以便跨设备迁移
- **FR-8 响应式界面**：桌面端与平板端正常使用；代码编辑器在移动端简化为只读+运行按钮
- **FR-9 离线可用性（部分）**：首次加载后 Pyodide 与课程内容缓存于浏览器；断网状态下可继续浏览已访问章节
- **FR-10 平台首页与个人中心**：首页含 Banner、课程卡片、推荐学习路径；个人中心展示积分、等级、徽章墙、学习统计

## Non-Functional Requirements
- **NFR-1 构建性能**：整站静态资源构建 ≤ 50MB（确保 Cloudflare Pages 免费方案构建时间 < 1 分钟）
- **NFR-2 首屏加载**：首屏 HTML/CSS ≤ 500KB；Pyodide 首次加载（按需触发）提示用户等待；LCP ≤ 3s
- **NFR-3 代码执行**：单次 Python 代码执行 ≤ 5s（超过提示"执行超时"）；支持安全沙箱（Pyodide 天然隔离）
- **NFR-4 浏览器兼容性**：Chrome/Edge ≥ 100、Firefox ≥ 100、Safari ≥ 15；需 WebAssembly 支持
- **NFR-5 可访问性**：主要文本颜色对比度 ≥ WCAG AA；代码编辑器提供深色模式
- **NFR-6 可维护性**：课程内容与代码解耦；新增课程仅需新增 Markdown 文件并重新构建，无需修改核心代码
- **NFR-7 部署零成本**：完全运行在 Cloudflare Pages 免费方案内，无额外服务器或数据库费用
- **NFR-8 代码质量**：前端 JS 模块化、无构建错误；HTML 语义化；CSS 使用自定义属性管理主题

## Constraints
- **Technical**: 前端静态站点 + 浏览器端 Pyodide；部署于 Cloudflare Pages；不得依赖付费后端服务；不得使用需要服务器端 Python 的框架（如 Django/Flask FastAPI 作为实时执行引擎）
- **Business**: 零运营成本；课程内容为开源/原创教学资源；无用户注册/登录系统（数据本地化）
- **Dependencies**: Pyodide（CDN 引入）、CodeMirror/Monaco 轻量编辑器、图表渲染（matplotlib 输出 base64 图像）

## Assumptions
- 用户使用现代浏览器（支持 WebAssembly 和 localStorage）
- 用户网络可访问 Pyodide CDN（jsDelivr 或官方 CDN）
- 课程内容由课程组在本地以 Markdown 编写并提交到 Git 仓库，通过 Git 触发 Cloudflare Pages 自动构建
- 学生之间不共享学习数据；教师通过课堂讲解配合平台使用，不依赖平台的教师端

## Acceptance Criteria

### AC-1: 课程体系完整可用
- **Given**: 学生首次访问平台首页
- **When**: 浏览课程列表并进入任一课程单元
- **Then**: 可看到至少 6 个课程单元，每个单元含 3+ 章节；每章节含学习目标、讲解内容、代码示例和小结
- **Verification**: `human-judgment`
- **Notes**: 由评审者检查课程列表页和随机 3 个章节内容结构

### AC-2: 浏览器端 Python 代码可运行
- **Given**: 学生打开包含代码编辑器的学习页面（Pyodide 已按需加载完成）
- **When**: 在编辑器中输入合法 Python 代码（如 `print("hello")`、`import pandas as pd; print(pd.__version__)`）并点击"运行"
- **Then**: 5 秒内在页面看到执行输出或图表；numpy/pandas/matplotlib 均可正常导入使用
- **Verification**: `programmatic`（通过模拟代码执行断言）+ `human-judgment`

### AC-3: 练习判分即时反馈
- **Given**: 学生进入某章节练习页面，代码编辑器内有预置题目与初始代码
- **When**: 学生完成代码并点击"检查答案"
- **Then**: 系统通过 Pyodide 运行预设测试用例，立即显示"正确/错误"及得分；全对练习的积分（+20）记入总分
- **Verification**: `programmatic`

### AC-4: 单元测评可完成并记录成绩
- **Given**: 学生完成某单元所有章节学习
- **When**: 进入单元测评页面，完成选择题和编程题后提交
- **Then**: 立即显示各题对错、总分（百分制）、薄弱知识点提示；测评成绩保存在本地存储
- **Verification**: `programmatic`

### AC-5: 积分与等级系统运转
- **Given**: 学生在平台上产生学习行为
- **When**: 完成章节、正确完成练习、通过测评等行为发生
- **Then**: 对应积分（10/20/50 等）累加；积分达到阈值时等级提升（Lv.1→Lv.10）；积分与等级在个人中心可见
- **Verification**: `programmatic`

### AC-6: 徽章解锁可触发并持久化
- **Given**: 学生满足某徽章解锁条件（如"完成首章"）
- **When**: 触发条件行为完成
- **Then**: 弹出"解锁新徽章"提示；徽章墙中对应徽章点亮；徽章状态持久化，刷新页面不丢失
- **Verification**: `programmatic`

### AC-7: 学习数据本地持久化与跨设备导入导出
- **Given**: 学生已学习多章并有积分/等级/徽章数据
- **When**: 在个人中心点击"导出学习数据"下载 JSON，在另一浏览器/设备点击"导入学习数据"上传该 JSON
- **Then**: 新设备个人中心显示与原设备一致的积分、等级、徽章和进度
- **Verification**: `programmatic`

### AC-8: 成功部署到 Cloudflare Pages 且在免费方案内运行
- **Given**: 代码提交至 Git 仓库并连接 Cloudflare Pages
- **When**: Cloudflare Pages 完成自动构建并部署
- **Then**: 构建日志显示构建时间 < 60 秒；部署成功后站点可通过 `*.pages.dev` 域名访问；首屏资源 < 500KB
- **Verification**: `programmatic`（检查构建日志与页面资源大小）

### AC-9: 响应式界面在桌面端与移动端可用
- **Given**: 学生在不同设备访问平台
- **When**: 使用桌面浏览器 ≥1280px 宽度和移动设备 ≤420px 宽度浏览首页和学习页
- **Then**: 桌面端显示完整目录树与编辑器；移动端布局适配竖屏、无横向滚动、主要按钮可点击
- **Verification**: `human-judgment`

### AC-10: 无障碍与深色模式
- **Given**: 学生切换至深色模式
- **When**: 浏览各页面与代码编辑器
- **Then**: 文本与背景对比度良好；代码编辑器支持深色语法高亮；主要操作按钮有足够尺寸与可辨识度
- **Verification**: `human-judgment`

## Open Questions
- [ ] 课程内容是团队自行编写还是基于现有公开 CC 协议资源改编？（影响初始课程覆盖度）
- [ ] 是否需要一个"课堂教师模式"（如课堂演示大屏、学生答题汇总）？（当前 PRD 未纳入，列为未来规划）
- [ ] 是否考虑接入 Cloudflare KV 实现跨设备同步（需少量 Workers 调用，仍在免费额度内）？（当前方案使用 localStorage）
- [ ] 是否需要对学生提交的代码进行安全性检查（Pyodide 本身在沙箱内运行，但可能消耗过多内存/CPU）？
- [ ] 课程内容版权与署名方式？（建议在课程页标注作者与许可证）
