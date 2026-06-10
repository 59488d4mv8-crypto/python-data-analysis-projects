# 商务数据分析在线教育平台 - The Implementation Plan (Decomposed and Prioritized Task List)

## [x] Task 1: 项目脚手架与静态站点结构搭建
- **Priority**: P0
- **Depends On**: None
- **Description**:
  - 创建项目目录结构：`index.html`（首页）、`courses/`（课程页）、`profile.html`（个人中心）、`quiz.html`（测评页）
  - 静态资源目录：`assets/css/`、`assets/js/`、`assets/data/`（课程内容 JSON）、`assets/images/`
  - 引入 Pyodide（CDN）、CodeMirror（或更轻量的自定义编辑器）、基础 JS 模块
  - 建立 `package.json` + Vite/Astro 等轻量构建工具（或纯静态不构建）
  - 增加 Cloudflare Pages 配置文件 `_redirects` 和 `_headers`
- **Acceptance Criteria Addressed**: AC-8, AC-9
- **Test Requirements**:
  - `programmatic` TR-1.1: 在本地运行开发服务器后，首页返回 200，控制台无 JS 错误
  - `programmatic` TR-1.2: `npm run build` 输出的 `dist/` 目录总大小 ≤ 5MB（不含课程数据），构建时间 < 30s
  - `human-judgement` TR-1.3: 首页布局整洁，导航栏、课程卡片区、底部信息区清晰可见
- **Notes**: 优先选择"零构建依赖"方案以缩短 Cloudflare Pages 构建时间；如使用 Markdown 课程内容，可通过轻量脚本在构建时预转为 HTML/JSON

## [x] Task 2: 课程内容数据结构与样例课程
- **Priority**: P0
- **Depends On**: Task 1
- **Description**:
  - 设计课程 JSON Schema：`{ course_id, title, description, units: [ { unit_id, title, chapters: [ { chapter_id, title, objectives, content, code_samples, exercises, summary } ] } ] }`
  - 编写至少 2 个课程单元、每单元 3 章的样例内容（Python 基础 → Pandas 基础），覆盖学习目标、知识讲解、代码示例、练习题目、小结
  - 课程数据写入 `assets/data/courses.json`，前端通过 `fetch` 异步加载
- **Acceptance Criteria Addressed**: AC-1, AC-2
- **Test Requirements**:
  - `programmatic` TR-2.1: courses.json 可通过 JSON Schema 校验，包含至少 2 个单元，每单元 ≥ 3 章节
  - `programmatic` TR-2.2: 浏览器访问课程页时，`fetch` 成功加载 courses.json 并渲染章节目录树
  - `human-judgement` TR-2.3: 课程内容结构完整（目标/讲解/代码示例/练习/小结），用语适合商务数据分析专业学生
- **Notes**: Markdown → JSON 的转换脚本放在 `scripts/build-courses.mjs`，避免引入重型解析库

## [ ] Task 3: 课程学习页面与目录树导航
- **Priority**: P0
- **Depends On**: Task 2
- **Description**:
  - 左侧目录树：展示课程→单元→章节层级，当前章节高亮，已完成章节打勾
  - 中部内容区：渲染学习目标、Markdown 讲解、代码示例、练习入口、小结
  - 底部"上一章 / 下一章 / 标记完成"按钮
  - URL 使用 Hash 路由（`#/course/c01/unit/u02/chapter/c03`），纯静态无需服务器路由
- **Acceptance Criteria Addressed**: AC-1, AC-9
- **Test Requirements**:
  - `programmatic` TR-3.1: 通过 Hash 路由访问任一章节，对应章节内容渲染且目录树高亮正确
  - `programmatic` TR-3.2: 点击"标记完成"后，localStorage 中 `progress[chapterId] = true`；刷新页面后该章显示已完成
  - `human-judgement` TR-3.3: 导航与内容区布局清晰，无横向滚动（桌面 ≥1280px）
- **Notes**: 路由方案可选 `history.pushState` + Cloudflare Pages `_redirects` 全部回退到 `index.html`

## [ ] Task 4: 互动代码编辑器与 Pyodide 集成
- **Priority**: P0
- **Depends On**: Task 1
- **Description**:
  - 嵌入 CodeMirror 6（轻量方案）或 `textarea + 语法高亮` 的极简编辑器
  - 封装 `pyodide-runner.js`：
    - 首次"运行"时异步加载 Pyodide（显示加载进度）
    - 预加载 numpy, pandas, matplotlib 包
    - 执行用户代码，捕获 stdout/stderr/traceback
    - 捕获 matplotlib 图表（转换为 base64 PNG）
    - 5 秒执行超时保护
  - 每个代码块独立运行环境（可重置命名空间）
- **Acceptance Criteria Addressed**: AC-2, AC-3
- **Test Requirements**:
  - `programmatic` TR-4.1: 在编辑器执行 `print("hello from pyodide")` → 输出面板显示该字符串，5 秒内返回
  - `programmatic` TR-4.2: 执行含语法错误代码 → 显示 Python traceback，页面不崩溃
  - `programmatic` TR-4.3: 执行 `import pandas as pd; df = pd.DataFrame({'a':[1,2]}); print(df)` → 正常输出 DataFrame
  - `programmatic` TR-4.4: 执行含 `plt.plot([1,2,3]); plt.show()` 的代码 → 页面渲染出 `<img>` 图表
  - `human-judgement` TR-4.5: 编辑器支持自动换行、行号、复制示例代码按钮；首次加载有清晰等待提示
- **Notes**: 使用官方 Pyodide CDN（`https://cdn.jsdelivr.net/pyodide/v0.26.2/full/pyodide.js`）；避免把 Pyodide 打包进构建产物

## [ ] Task 5: 练习系统（题目 + 测试用例 + 即时判分）
- **Priority**: P0
- **Depends On**: Task 2, Task 4
- **Description**:
  - 课程 JSON 中每章节 `exercises` 字段：`{ exerciseId, prompt, starterCode, testCode, hints }`
  - 练习页面在代码编辑器中显示 `starterCode`，提示学生补全
  - 学生点击"检查答案"：拼接学生代码 + `testCode` → 通过 Pyodide 执行 → 断言通过为正确
  - 得分逻辑：每道练习按测试用例数均分给分；章节练习全对 +20 积分
- **Acceptance Criteria Addressed**: AC-3, AC-5
- **Test Requirements**:
  - `programmatic` TR-5.1: 提供一个已知正确答案的练习 → "检查答案"返回"全部正确"并加 20 分
  - `programmatic` TR-5.2: 提供一个错误答案（如返回 None） → "检查答案"显示具体失败的断言与期望/实际值
  - `programmatic` TR-5.3: 同一练习多次提交仅在"首次全对"时加 +20 积分（防刷分）
  - `human-judgement` TR-5.4: 练习判分反馈界面友好，包含错误提示与"查看参考答案"按钮
- **Notes**: `testCode` 中的断言使用标准 `assert`，由 Pyodide 捕获 `AssertionError`

## [ ] Task 6: 单元测评系统（选择 + 编程题）
- **Priority**: P1
- **Depends On**: Task 5
- **Description**:
  - 测评数据结构：`{ quizId, title, questions: [ { type: 'choice'|'coding', ... } ] }`
  - 选择题：题干 + 选项 + 正确答案索引 + 解析 → 学生提交后即时判分
  - 编程题：类似练习，但题面更复杂、测试用例更多
  - 测评结束页面显示得分（百分制）、每道题对错、薄弱知识点标签
  - 测评 ≥ 80 分 +50 积分；首次通关解锁"测评达人"徽章条件
- **Acceptance Criteria Addressed**: AC-4, AC-5
- **Test Requirements**:
  - `programmatic` TR-6.1: 一份全对答案 → 得分 100，+50 积分入账
  - `programmatic` TR-6.2: 一份 60 分答案 → 显示薄弱知识点标签，不加 50 积分，但测评成绩保存在 localStorage
  - `programmatic` TR-6.3: 已提交测评可在个人中心查看历史得分
  - `human-judgement` TR-6.4: 测评题目难度与课程内容匹配，编程题不超过 3 道以避免学生浏览器负担
- **Notes**: 测评数据也存储在 `assets/data/` 下，按单元分文件以减小首屏加载

## [ ] Task 7: 成就激励系统（积分 / 等级 / 徽章 / 统计）
- **Priority**: P1
- **Depends On**: Task 3, Task 5, Task 6
- **Description**:
  - `achievements.js` 模块：
    - 积分事件：`awardPoints(key, amount)` 去重记录（每类事件每个章节/练习/测评仅一次）
    - 等级表：Lv.1=0, Lv.2=100, Lv.3=300, Lv.4=600, Lv.5=1000, Lv.6=1500, Lv.7=2200, Lv.8=3000, Lv.9=4000, Lv.10=5000
    - 徽章定义与触发条件：`first_chapter, first_perfect_exercise, first_quiz_pass, streak_7_days, hours_10, all_courses_done` 等 6 枚
    - 学习时长：每 30 秒记录一次当前页面停留（去重）
  - 徽章解锁 Toast 弹窗；个人中心徽章墙点亮/未点亮两种状态
- **Acceptance Criteria Addressed**: AC-5, AC-6
- **Test Requirements**:
  - `programmatic` TR-7.1: 完成第一章 → 积分 +10，徽章 `first_chapter` 解锁并持久化
  - `programmatic` TR-7.2: 积分达到 100 → 等级自动提升到 Lv.2，等级徽章更新
  - `programmatic` TR-7.3: 模拟 7 天连续学习数据 → `streak_7_days` 徽章解锁
  - `programmatic` TR-7.4: 刷新页面 → 个人中心积分/等级/徽章与刷新前一致
  - `human-judgement` TR-7.5: 徽章图形设计简洁美观；等级进度条直观
- **Notes**: 徽章使用 SVG icon 或 emoji，不引入图片资源以减小体积

## [ ] Task 8: 学习数据持久化与导入/导出
- **Priority**: P1
- **Depends On**: Task 7
- **Description**:
  - `storage.js` 模块：统一管理 localStorage 读写，命名空间 `dae_edu_v1_`
  - 数据 Schema：`{ points, level, badges: {badgeId:{unlockedAt,...}}, progress: {chapterId:{done,lastVisit}}, exercises: {exerciseId:{correct,attempts}}, quizzes: {quizId:{score,submittedAt}}, stats: {totalMinutes, dailyActivity} }`
  - 个人中心"导出数据"→ 下载 JSON；"导入数据"→ 选择文件读取并合并/覆盖
- **Acceptance Criteria Addressed**: AC-7
- **Test Requirements**:
  - `programmatic` TR-8.1: 点击"导出" → 下载有效 JSON 文件，结构包含积分/等级/徽章/进度
  - `programmatic` TR-8.2: 新浏览器导入该 JSON → 个人中心显示一致的积分与徽章
  - `programmatic` TR-8.3: localStorage 满量异常情况 → 捕获异常并提示
  - `human-judgement` TR-8.4: 导入/导出流程有明确提示与二次确认，避免误操作
- **Notes**: 导入时提供"合并"与"覆盖"两种模式

## [ ] Task 9: 首页与个人中心 UI 完善
- **Priority**: P1
- **Depends On**: Task 1, Task 7
- **Description**:
  - 首页：Banner（平台介绍 + 开始学习按钮）、课程卡片列表（显示每门课完成度百分比）、推荐学习路径、学习状态总览（积分/等级/今日学习时长）
  - 个人中心：等级卡片（含进度条）、积分明细、徽章墙、学习统计卡片（学习天数、完成章节、练习正确率、测评平均得分）、导入/导出按钮、主题切换
- **Acceptance Criteria Addressed**: AC-9, AC-10
- **Test Requirements**:
  - `programmatic` TR-9.1: 首页课程卡片显示的完成度与 localStorage 中数据一致
  - `programmatic` TR-9.2: 切换主题 → CSS 变量更新，刷新后仍保持所选主题
  - `human-judgement` TR-9.3: 首页和个人中心视觉统一；在 1920×1080 和 1366×768 两种分辨率下无布局错乱
  - `human-judgement` TR-9.4: 个人中心数据可视化（如正确率曲线）直观易读

## [ ] Task 10: 响应式与无障碍优化、深色模式
- **Priority**: P2
- **Depends On**: Task 9
- **Description**:
  - 响应式：移动端（≤ 768px）目录树折叠为汉堡菜单；代码编辑器高度自适应
  - 深色模式：CSS 自定义属性（`--bg, --text, --code-bg` 等）；`prefers-color-scheme` 自动检测 + 手动切换
  - 无障碍：图片加 alt；表单控件加 label；键盘导航完整；颜色对比度 ≥ AA
- **Acceptance Criteria Addressed**: AC-9, AC-10
- **Test Requirements**:
  - `human-judgement` TR-10.1: Chrome DevTools 模拟 iPhone 12 / iPad / 1920px 桌面 → 三个断点下布局无明显问题
  - `human-judgement` TR-10.2: 深色模式下正文和代码编辑器对比度良好，不刺眼
  - `programmatic` TR-10.3: Lighthouse 无障碍分数 ≥ 80
- **Notes**: 不追求像素级完美，优先保证可用性

## [ ] Task 11: 课程内容扩充到 6 个单元
- **Priority**: P2
- **Depends On**: Task 2, Task 4, Task 5
- **Description**:
  - 扩充课程体系至 6 单元：
    1. Python 基础与数据类型（4 章）
    2. NumPy 数值计算（3 章）
    3. Pandas 数据处理（4 章）
    4. matplotlib / seaborn 数据可视化（3 章）
    5. 商务统计分析（描述统计、假设检验、相关性）（4 章）
    6. 商业案例实战（销售分析、用户行为分析、库存分析）（4 章）
  - 每章至少 1-2 个代码示例和 2-5 道练习；每个单元配 1 个测评（5 选择 + 2 编程）
- **Acceptance Criteria Addressed**: AC-1, AC-3, AC-4
- **Test Requirements**:
  - `programmatic` TR-11.1: courses.json 含 6 单元、总章节数 ≥ 22
  - `programmatic` TR-11.2: 每个代码示例在 Pyodide 中可运行（通过 CI 脚本 smoke-test）
  - `human-judgement` TR-11.3: 课程内容循序渐进，适合商务数据分析专业学生起点
- **Notes**: 课程内容为长期任务，MVP 阶段先完成前 3 单元 + 样例数据

## [ ] Task 12: Cloudflare Pages 部署配置与构建脚本
- **Priority**: P0
- **Depends On**: Task 1
- **Description**:
  - 项目根目录添加 `package.json` 的 `scripts.build` 命令
  - Cloudflare Pages 项目配置：构建命令 `npm run build`、输出目录 `dist/`（或根目录 `./` 若纯静态）
  - 添加 `public/_headers` 设置安全头与缓存策略（HTML no-cache, CSS/JS 长缓存 + hash）
  - 添加 `public/_redirects` 将所有路由回退到 `index.html`（SPA 风格）
  - 编写 README / 部署说明（部署流程、Git 分支策略）
- **Acceptance Criteria Addressed**: AC-8
- **Test Requirements**:
  - `programmatic` TR-12.1: 本地 `npm run build` 成功，`dist/` 总大小 ≤ 50MB（首版课程+静态资源）
  - `programmatic` TR-12.2: Cloudflare Pages 构建日志时长 < 60 秒
  - `human-judgement` TR-12.3: `*.pages.dev` 域名首页可访问，学习页路由跳转正常
- **Notes**: 关键：确保构建时间控制在 1 分钟内；Pyodide 通过 CDN 加载，不纳入构建产物

## [ ] Task 13: 测试与质量保障
- **Priority**: P2
- **Depends On**: Task 1–Task 12
- **Description**:
  - 端到端冒烟测试（可选）：使用 Playwright/Node 脚本验证首页加载、课程加载、代码执行、练习判分、积分累加
  - JS 模块的轻量单元测试（`vitest` 或简易 Node 测试），覆盖积分、等级、徽章、storage 模块
  - 代码风格统一（ESLint + Prettier 可选）
- **Acceptance Criteria Addressed**: AC-2, AC-3, AC-5, AC-7
- **Test Requirements**:
  - `programmatic` TR-13.1: 关键模块单元测试全部通过
  - `programmatic` TR-13.2: 冒烟测试脚本能成功走完"首页 → 课程 → 运行代码 → 练习判分 → 查看积分"一条路径
  - `human-judgement` TR-13.3: 代码评审通过；关键逻辑有注释
- **Notes**: 不追求 100% 测试覆盖率，优先保障核心学习流程
