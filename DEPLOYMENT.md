# 灰狗巴士项目 - 部署指南

## 📋 项目概述

这是一个基于Flask的Web应用，可以自动从YouTube抓取美国城市介绍视频，生成中英双语内容。

## 🚀 快速启动（本地开发）

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动应用

```bash
python app.py --web
```

应用将在 `http://localhost:8000` 启动

## ☁️ 部署方案

### 方案一：Docker 部署（推荐）

#### 1. 创建 Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "app.py", "--web"]
```

#### 2. 构建和运行

```bash
# 构建镜像
docker build -t greyhound-lines .

# 运行容器
docker run -d -p 8000:8000 --name greyhound-app greyhound-lines

# 查看日志
docker logs -f greyhound-app
```

### 方案二：Heroku 部署

#### 1. 准备文件

创建 `Procfile`：
```
web: gunicorn app:app --preload --workers 1 --timeout 300
```

创建 `runtime.txt`：
```
python-3.9.12
```

更新 `requirements.txt`，添加：
```
gunicorn==20.1.0
```

#### 2. 部署步骤

```bash
# 安装 Heroku CLI
# 登录
heroku login

# 创建应用
heroku create your-app-name

# 部署
git add .
git commit -m "Initial deploy"
git push heroku main

# 打开应用
heroku open
```

### 方案三：Vercel 部署（Serverless）

#### 1. 创建 `vercel.json`

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

#### 2. 修改 `app.py`

确保 `app.run()` 只在直接运行时执行：

```python
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--web':
        print("Starting web server on http://localhost:8000")
        run_flask()
    elif len(sys.argv) > 1 and sys.argv[1] == '--once':
        scheduler.run_once()
    # 移除默认启动定时任务的逻辑，只保留web服务
```

### 方案四：AWS EC2 部署

#### 1. 启动 EC2 实例

- 选择 Ubuntu 20.04 LTS
- 配置安全组，开放 8000 端口

#### 2. 连接并设置

```bash
# 连接
ssh -i your-key.pem ubuntu@your-ec2-ip

# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Python
sudo apt install python3-pip python3-venv -y

# 克隆项目
git clone your-repo-url
cd Greyhound_Lines

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 使用 Gunicorn
pip install gunicorn

# 创建 systemd 服务
sudo nano /etc/systemd/system/greyhound.service
```

#### 3. systemd 服务配置

```
[Unit]
Description=Greyhound Lines Web App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/Greyhound_Lines
Environment="PATH=/home/ubuntu/Greyhound_Lines/venv/bin"
ExecStart=/home/ubuntu/Greyhound_Lines/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 app:app --timeout 300
Restart=always

[Install]
WantedBy=multi-user.target
```

#### 4. 启动服务

```bash
sudo systemctl daemon-reload
sudo systemctl start greyhound
sudo systemctl enable greyhound
sudo systemctl status greyhound
```

#### 5. 配置 Nginx 反向代理（可选）

```bash
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/greyhound
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 300s;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/greyhound /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 🔧 环境配置

### 生产环境优化

1. **使用生产级 WSGI 服务器**：Gunicorn + Nginx
2. **设置合理的超时时间**：YouTube API 调用可能需要较长时间
3. **添加缓存**：对生成的内容进行缓存，避免重复调用
4. **日志记录**：配置 proper logging

### 配置文件

可以添加 `.env` 文件来管理配置：

```env
FLASK_ENV=production
PORT=8000
OUTPUT_DIR=./output
```

## 📊 性能优化建议

1. **内容缓存**：使用 Redis 或文件缓存已生成的内容
2. **异步处理**：使用 Celery 异步生成内容，避免阻塞请求
3. **CDN**：使用 CDN 加速静态资源
4. **数据库**：将生成的内容存储到数据库中

## 🛡️ 安全建议

1. **HTTPS**：使用 Let's Encrypt 配置 SSL
2. **限流**：添加 API 限流，防止滥用
3. **CORS**：配置适当的 CORS 策略
4. **环境变量**：不将敏感信息提交到代码库

## 📝 监控和维护

1. **应用监控**：使用 Sentry、New Relic 等工具
2. **日志管理**：集中管理日志
3. **定期更新**：更新依赖包，修复安全漏洞

## 🎯 推荐方案

对于快速上线，推荐使用 **Docker + VPS** 或 **Heroku**。

需要帮助部署到特定平台？请告诉我！
