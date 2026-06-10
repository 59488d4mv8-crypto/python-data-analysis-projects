# 商务数据分析在线教育平台 - 验收清单 (Checklist)

## 基础部署 & 可访问性

- [ ] Checkpoint 1: 项目可通过 `npm run build`（或同等命令）构建成功，构建输出目录包含完整静态资源
- [ ] Checkpoint 2: Cloudflare Pages 构建日志显示构建时长 < 60 秒，部署成功
- [ ] Checkpoint 3: 站点通过 `*.pages.dev` 域名可正常访问，首屏 3 秒内完成渲染
- [ ] Checkpoint 4: 首屏 HTML/CSS/JS 总资源 ≤ 500KB（未加载课程数据与 Pyodide 时）
- [ ] Checkpoint 5: 在 Chrome/Edge/Firefox/Safari 最新版浏览器打开首页无 JS 异常

## 课程体系与导航

- [ ] Checkpoint 6: 课程列表页展示至少 6 个课程单元，每个单元显示标题、简介、完成度
- [ ] Checkpoint 7: 进入任一课程单元后，左侧目录树显示完整章节结构（≥ 3 章/单元）
- [ ] Checkpoint 8: 目录树点击章节可切换到对应内容，URL Hash 更新，当前章节高亮
- [ ] Checkpoint 9: 每个章节页面包含"学习目标 / 知识讲解 / 代码示例 / 练习入口 / 小结"等结构区块
- [ ] Checkpoint 10: 底部"上一章 / 下一章 / 标记完成"按钮功能正常，边界章节正确禁用

## 互动代码编辑器 & Pyodide

- [ ] Checkpoint 11: 代码编辑器带行号与语法高亮，可自由编辑 Python 代码
- [ ] Checkpoint 12: 点击"运行"后，若 Pyodide 未加载，显示加载进度；加载完成后执行代码
- [ ] Checkpoint 13: 执行简单打印语句后 5 秒内输出正确内容
- [ ] Checkpoint 14: `import numpy, pandas, matplotlib` 均可成功，不报错
- [ ] Checkpoint 15: 使用 `matplotlib` 绘图的代码块执行后，页面内渲染出图片
- [ ] Checkpoint 16: 执行含语法错误/异常的代码，页面显示 Python 报错堆栈，不崩溃
- [ ] Checkpoint 17: 长时间循环/大计算代码在 5 秒超时后终止并提示"执行超时"

## 练习系统

- [ ] Checkpoint 18: 每章节至少 2 道练习，含题目描述、起始代码、检查按钮
- [ ] Checkpoint 19: 对练习提交正确答案 → 系统判为"正确"并累加得分；+20 积分入账（首次全对）
- [ ] Checkpoint 20: 提交错误答案 → 显示具体失败断言信息与期望输出
- [ ] Checkpoint 21: 同一练习重复提交正确答案不会重复加积分
- [ ] Checkpoint 22: "查看提示"与"查看参考答案"按钮工作正常

## 单元测评

- [ ] Checkpoint 23: 每单元包含 1 份测评，题目含选择题（≥ 3 道）与编程题（≥ 2 道）
- [ ] Checkpoint 24: 选择题提交后即时显示对错与正确答案解析
- [ ] Checkpoint 25: 编程题通过 Pyodide 执行测试用例判分，显示每题得分
- [ ] Checkpoint 26: 测评结束显示总分（百分制）与薄弱知识点标签
- [ ] Checkpoint 27: 测评成绩保存到本地存储，可在个人中心查看历史分数
- [ ] Checkpoint 28: 首次测评 ≥ 80 分 → 解锁"测评达人"徽章并 +50 积分

## 成就激励系统

- [ ] Checkpoint 29: 完成 1 章学习（点击"标记完成"）→ 积分 +10，进度保存
- [ ] Checkpoint 30: 积分达到 Lv.2 阈值（100） → 等级自动提升，顶部与个人中心等级图标更新
- [ ] Checkpoint 31: 满足徽章触发条件（首章、首满分练习、首测评通关、连续 7 天、累计 10 小时、全课完成） → 徽章墙点亮，Toast 弹窗提示
- [ ] Checkpoint 32: 刷新页面后，积分 / 等级 / 徽章 / 进度保持不变
- [ ] Checkpoint 33: 个人中心显示累计学习时长、完成章节数、练习正确率、测评平均得分

## 数据持久化 & 导入 / 导出

- [ ] Checkpoint 34: localStorage 中所有数据以统一前缀（如 `dae_edu_v1_`）存储，结构清晰
- [ ] Checkpoint 35: 个人中心"导出学习数据"可下载 JSON 文件，文件内容含积分 / 等级 / 徽章 / 进度 / 测评成绩
- [ ] Checkpoint 36: 新浏览器/设备"导入学习数据"并选择该 JSON 文件 → 个人中心数据与原设备一致
- [ ] Checkpoint 37: 导入时提供"合并"与"覆盖"两种模式，且有二次确认

## 响应式 & 深色模式 & 无障碍

- [ ] Checkpoint 38: 桌面 ≥ 1280px 分辨率下，目录树 + 内容区 + 代码编辑器三栏布局正常
- [ ] Checkpoint 39: 移动 ≤ 420px 下，目录折叠为菜单，主要按钮可点击，无横向滚动
- [ ] Checkpoint 40: 深色模式下文本/背景对比度良好，代码编辑器配色适配深色
- [ ] Checkpoint 41: 主题切换状态持久化，刷新仍保留
- [ ] Checkpoint 42: 主要交互元素支持键盘操作（Tab 键切换、Enter 激活）
- [ ] Checkpoint 43: 图片有 alt，表单控件有 label

## 课程内容质量

- [ ] Checkpoint 44: 课程覆盖 Python 基础 / NumPy / Pandas / 可视化 / 统计分析 / 商业案例 6 大模块
- [ ] Checkpoint 45: 总章节数 ≥ 22，每章配备学习目标与小结
- [ ] Checkpoint 46: 所有代码示例块均可在 Pyodide 中正常执行
- [ ] Checkpoint 47: 课程语言风格适合商务数据分析专业学生，包含恰当的商业场景案例

## 代码质量 & 可维护性

- [ ] Checkpoint 48: 前端 JS 模块结构清晰（`pyodide-runner.js` / `storage.js` / `achievements.js` 等职责分明）
- [ ] Checkpoint 49: 课程数据与渲染逻辑解耦，新增/修改课程不改动核心 JS 代码
- [ ] Checkpoint 50: 关键功能（积分累加、徽章判定、练习判分）有单元测试或手动验证通过
- [ ] Checkpoint 51: 部署文档（README 或部署说明）描述 Cloudflare Pages 配置步骤
