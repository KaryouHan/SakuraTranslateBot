# SakuraTranslateBot

一个 Telegram 小机器人：在私聊或群聊里收到中文消息后，自动把每一句翻译成日语，并作为回复发在原消息下面。

## 能做到什么

- 私聊：你发中文，机器人回复日语。
- 群聊：群友发中文，机器人在那条消息下面回复日语。
- 多句中文：会尽量逐句对应，输出为「中文」下一行「日语」。
- 非中文消息：默认忽略。

注意：Telegram 机器人不能直接修改别人发出的消息，所以不能真的把翻译“塞进同一条消息里”。最接近、也最稳定的做法是让机器人 reply 原消息。

## 准备

你需要两个 key：

1. Telegram Bot Token
   - 在 Telegram 里找 `@BotFather`
   - 发送 `/newbot`
   - 按提示创建机器人
   - 复制它给你的 token

2. Google Gemini API Key
   - 用来做中文到日语翻译

## 安装

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

编辑 `.env`：

```bash
TELEGRAM_BOT_TOKEN=你的_telegram_bot_token
LLM_API_KEY=你的_gemini_api_key
LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
LLM_MODEL=gemini-2.5-flash-lite
```

## 运行

```bash
source .venv/bin/activate
python bot.py
```

看到 `SakuraTranslateBot is running...` 后，就可以去 Telegram 和机器人聊天。


## 两种运行模式

### 1. 普通 Bot 模式

运行：

```bash
source .venv/bin/activate
python bot.py
```

这个模式只能处理机器人能看到的聊天。机器人必须被加入群聊；如果要看见所有普通消息，需要在 `@BotFather` 里关闭 `Group Privacy`。

### 2. 个人账号模式，也就是截图那种效果

运行：

```bash
source .venv/bin/activate
python userbot.py
```

这个模式会登录你的 Telegram 账号，监听你自己发出的中文消息，然后自动编辑这条原消息，在中文下面追加一段 Telegram 引用样式的日语翻译。它可以作用于你的私聊、群聊、频道评论等你账号本来就能发言的地方。

第一次运行会要求输入手机号、Telegram 验证码，可能还会要求两步验证密码。登录成功后，会生成一个 `sakura_translate.session` 本地会话文件，之后不用每次重新登录。这个文件等同于登录状态，不要发给别人。

你还需要在 `.env` 加上：

```bash
TELEGRAM_API_ID=你的_api_id
TELEGRAM_API_HASH=你的_api_hash
TELEGRAM_SESSION_NAME=sakura_translate
```

`TELEGRAM_API_ID` 和 `TELEGRAM_API_HASH` 在这里申请：

```text
https://my.telegram.org/apps
```

注意：个人账号模式是用你的账号自动发消息。请只用于正常翻译，不要高频刷屏或用于陌生群骚扰。

## 放进群里

1. 把机器人加入群聊。
2. 如果你想让它自动翻译所有人的中文消息，需要去 `@BotFather`：
   - `/mybots`
   - 选择你的 bot
   - `Bot Settings`
   - `Group Privacy`
   - 选择 `Turn off`
3. 重新把机器人拉进群，或者让它重新加入。

如果不关闭 privacy mode，机器人通常只能看到命令、@ 它的消息、以及回复它的消息。

## 使用方式

发：

```text
小龙虾给我做的
```

机器人回：

```text
小龙虾给我做的
ザリガニが私に作ってくれたんだ
```

## 可选配置

`.env` 支持这些变量：

```bash
TELEGRAM_BOT_TOKEN=
LLM_API_KEY=
LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
LLM_MODEL=gemini-2.5-flash-lite
TARGET_LANGUAGE=Japanese
SOURCE_LANGUAGE=Chinese
BOT_REPLY_MODE=paired
```

`BOT_REPLY_MODE`：

- `paired`：中文下一行日语，适合对照。
- `translation_only`：只回复日语。
