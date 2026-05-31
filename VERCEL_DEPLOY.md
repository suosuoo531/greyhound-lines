# Vercel 部署指南

## 📋 前置准备

1. **GitHub 账号**（推荐）或 GitLab/Bitbucket
2. **Vercel 账号** - 访问 https://vercel.com 注册
3. **Git** 已安装

## 🚀 部署步骤（使用 Vercel Dashboard）

### 方法一：通过 Vercel Dashboard（最简单）

#### 1. 上传项目到 GitHub

```bash
# 初始化 Git
git init
git add .
git commit -m "Initial commit: Greyhound Lines"

# 创建 GitHub 仓库，然后推送到 GitHub
git remote add origin https://github.com/your-username/greyhound-lines.git
git branch -M main
git push -u origin main
```

#### 2. 在 Vercel 中导入项目

1. 访问 https://vercel.com/dashboard
2. 点击 **"Add New"** → **"Project"**
3. 点击 **"Import"** 选择你的 GitHub 仓库
4. 配置项目设置：
   - **Project Name**: 输入项目名称（如 `greyhound-lines`）
   - **Framework Preset**: 保持 `Other`
   - **Root Directory**: 保持为空
   - **Build Command**: 留空
   - **Output Directory**: 留空
5. 点击 **"Deploy"**

#### 3. 等待部署完成

- 部署通常需要 1-2 分钟
- 部署成功后会获得一个 URL（如 `https://greyhound-lines.vercel.app`）

### 方法二：使用 Vercel CLI

#### 1. 安装 Vercel CLI

```bash
npm i -g vercel
```

#### 2. 登录并部署

```bash
# 登录
vercel login

# 在项目目录中部署
vercel

# 按照提示操作：
# - Set up and deploy? → Y
# - Which scope? → 选择你的账号
# - Link to existing project? → N
# - Project name → greyhound-lines
# - In which directory is your code located? → ./
# - Want to modify these settings? → N

# 部署后，会获得预览 URL
```

#### 3. 部署到生产环境

```bash
vercel --prod
```

## ⚙️ Vercel 配置说明

### 项目结构

```
Greyhound_Lines/
├── api/
│   └── index.py          # Vercel Serverless API
├── static/               # 静态文件
│   ├── index.html
│   ├── style.css
│   └── app.js
├── vercel.json           # Vercel 配置
├── requirements.txt      # Python 依赖
├── config.py
├── youtube_scraper.py
├── content_processor.py
└── scheduler.py
```

### vercel.json 配置说明

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/**/*.py",
      "use": "@vercel/python"
    },
    {
      "src": "static/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "/static/$1"
    }
  ]
}
```

## 🎯 关键注意事项

### 1. 超时限制

- Vercel Serverless Function 的**最大执行时间是 10 秒**（免费版）
- YouTube API 调用可能超过这个时间！

**解决方案**：
- 添加缓存机制
- 使用异步处理
- 考虑使用其他平台（如 Heroku、AWS）处理长时间任务

### 2. 环境变量

在 Vercel Dashboard 中可以设置环境变量：
1. 进入项目设置
2. 点击 **Environment Variables**
3. 添加需要的变量

### 3. 依赖问题

确保 `requirements.txt` 包含所有依赖：
```
pytube>=15.0.0
youtube-transcript-api>=0.6.0
deep-translator>=1.11.0
Flask>=2.3.0
```

## 🔧 调试部署问题

### 查看部署日志

1. 在 Vercel Dashboard 进入项目
2. 点击 **"Deployments"** 标签
3. 选择最近的部署
4. 查看 **"Functions"** 日志

### 本地测试 API

```bash
# 测试本地服务器是否正常
python app.py --web

# 测试 API
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"location": "New York City"}'
```

## 🚀 快速开始（完整命令）

```bash
# 1. 创建项目目录（如果还没有）
cd Greyhound_Lines

# 2. 初始化 Git
git init
git add .
git commit -m "Initial commit"

# 3. 在 GitHub 创建仓库（网页操作）

# 4. 推送到 GitHub
git remote add origin https://github.com/你的用户名/greyhound-lines.git
git branch -M main
git push -u origin main

# 5. 到 Vercel 导入并部署！
```

## ⚠️ Vercel 限制说明

| 限制 | 免费版 | Pro 版 |
|------|--------|--------|
| Serverless Function 超时 | 10s | 60s |
| 带宽 | 100GB | 1TB |
| 部署次数 | 无限 | 无限 |

**如果 YouTube API 调用经常超时，建议使用 Heroku 或 Docker 部署到 VPS**。

## 📚 更多资源

- Vercel 文档: https://vercel.com/docs
- Vercel Python: https://vercel.com/docs/runtimes#official-runtimes/python
- Flask + Vercel: https://github.com/vercel/examples/tree/main/python/flask

需要帮助？告诉我！
