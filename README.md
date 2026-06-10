# PyDataEdu · Python 商务数据分析在线教育平台

纯静态站点,基于原生 HTML / CSS / JS,通过 Pyodide (CDN) 在浏览器内运行 Python,面向商务 / 金融数据分析教学。零构建工具、零框架、零 TypeScript。

## 目录结构

```
.
├── index.html       # 首页
├── course.html      # 课程学习
├── profile.html     # 个人中心
├── quiz.html        # 测评
├── assets/
│   ├── css/style.css
│   ├── js/app.js
│   └── data/courses.json
├── _redirects       # Cloudflare Pages SPA 回退
├── _headers         # 安全头 / 缓存策略
├── package.json
└── README.md
```

## 开发

```bash
npm install
npm run dev      # 启动本地开发服务器 http://localhost:8080
npm run build    # 输出静态产物,无构建步骤,仅验证可部署
```

## Cloudflare Pages 配置

- **构建命令(Build command): `npm run build`
- **输出目录(Build output directory)**: `./` 或 `dist/`
- Pyodide 在 `index.html` / `course.html` / `profile.html` / `quiz.html` 的 `<head>` 中以注释形式预留,正式上线时在代码执行模块中懒加载即可。
