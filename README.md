# Greyhound Lines - 美国城市之旅 🚌

一个定时从YouTube抓取美国州/城市介绍视频并生成中英双语内容的订阅系统，配有精美的灰狗巴士风格UI界面。

## 功能特性

- 🎨 **精美UI界面** - 灰狗巴士风格的Web界面
- 🔄 **定时执行** - 每周一、周三自动运行
- 🎯 **随机选择** - 从50个州和20个主要城市中随机选择
- 📹 **视频搜索** - 自动搜索相关的旅游介绍视频
- 📝 **字幕获取** - 提取视频字幕并生成摘要
- 🌐 **双语翻译** - 自动翻译成中文，生成中英双语Markdown文档
- 💾 **自动保存** - 输出文件保存在 `output/` 目录
- 🌍 **Web服务器** - 内置Flask服务器，随时查看

## 安装

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 复制环境变量示例文件：
```bash
cp .env.example .env
```

## 使用方法

### 启动Web服务器（推荐）
```bash
python main.py
```
然后访问 http://localhost:8000 查看界面

### 仅启动Web服务器
```bash
python main.py --web
```

### 立即执行一次（测试用）
```bash
python main.py --once
```

## 配置

可以在 `config.py` 中修改配置：
- `OUTPUT_DIR`: 输出目录
- `US_STATES`: 美国州列表
- `US_CITIES`: 美国城市列表
- `SCHEDULE_DAYS`: 执行的星期几
- `SCHEDULE_TIME`: 执行时间

## 输出

生成的内容保存在 `output/` 目录下，文件格式为 `{Location}_{timestamp}.md`

## UI特色

- 🚌 灰狗巴士品牌配色（蓝白主题）
- 🎬 巴士动画效果
- 🗺️ 城市路线展示
- 📖 双语内容并排显示
- 🏙️ 热门目的地卡片
