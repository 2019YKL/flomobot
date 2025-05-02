# flomo bot

Note: 官方已支持 Telegram 发送到 Flomo，详情见 <https://help.flomoapp.com/advance/extension/tgbot>

使用 Telegram 机器人发送笔记到你的 Flomo. 你需要有一台可访问 Telegram 的服务器。

## 准备工作

1. @BotFather 新建机器人，获取 token
2. Flomo 官网获取 API，链接 <https://flomoapp.com/mine?source=incoming_webhook>
3. 通过 @userinfobot Bot 获取你的 UserID
4. `cp config-example.py config.py`, 修改对应字段为前三步获取的值

## 运行方式（本地）

1. 安装依赖 `pip install -r requirements.txt`
2. `python floambot.py`

## 运行方式（Docker）

### 使用 docker-compose（推荐）

1. 确保已安装 Docker 和 docker-compose
2. 在项目目录下运行：
   ```
   docker-compose up -d
   ```
3. 查看日志：
   ```
   docker-compose logs -f
   ```
4. 停止服务：
   ```
   docker-compose down
   ```

### 使用 Docker 命令

1. 构建镜像：
   ```
   docker build -t flomobot .
   ```
2. 运行容器：
   ```
   docker run -d --name flomobot -v $(pwd)/config.py:/app/config.py flomobot
   ```
3. 查看日志：
   ```
   docker logs -f flomobot
   ```
4. 停止并删除容器：
   ```
   docker stop flomobot && docker rm flomobot
   ```

## 使用方法

给新建的机器人发送消息，机器人会将内容发送到 Flomo 并回复包含访问链接的成功消息。

PS:

[Flomo](https://flomoapp.com/) 是一个崇尚无压输入的笔记工具，欢迎使用我的邀请链接注册 <https://flomoapp.com/register2/?Njg4NQ>
