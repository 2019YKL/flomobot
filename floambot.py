#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.
#
# THIS EXAMPLE HAS BEEN UPDATED TO WORK WITH THE BETA VERSION 12 OF PYTHON-TELEGRAM-BOT.
# If you're still using version 11.1.0, please see the examples at
# https://github.com/python-telegram-bot/python-telegram-bot/tree/v11.1.0/examples

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import datetime
import os
import requests
from config import *

from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes
from telegram.ext.filters import TEXT

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
async def start(update, context):
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Hi!')


async def help(update, context):
    """Send a message when the command /help is issued."""
    await update.message.reply_text('Help!')


async def echo(update, context):
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

async def flomo(update, context):
    """Add the user message to flomo using API."""
    chat_id = update.message.chat.id
    if (chat_id != int(CHAT_ID)):
        await update.message.reply_text('You are not the owner of this bot.')
    else:
        # 获取用户消息内容
        content = update.message.text
        
        # 准备API请求数据
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            'content': content
        }
        
        # 发送POST请求到flomo API
        import json
        response = requests.post(FLOMO_API, headers=headers, data=json.dumps(data))
        
        # 只返回简洁的成功信息和链接
        if response.status_code == 200:
            try:
                # 解析响应JSON
                response_data = response.json()
                
                # 如果有memo字段且有slug字段
                if 'memo' in response_data and 'slug' in response_data['memo']:
                    # 提取slug并构建flomo链接
                    slug = response_data['memo']['slug']
                    link = f'https://v.flomoapp.com/mine/?memo_id={slug}'
                    # 使用Telegram的Markdown格式将链接嵌入到文字中
                    await update.message.reply_text(f'🎉 发送成功 🔗 [访问链接]({link})', parse_mode='Markdown')
                else:
                    await update.message.reply_text('发送成功！')
            except Exception as e:
                await update.message.reply_text('发送成功！')
        else:
            await update.message.reply_text(f'发送失败，状态码: {response.status_code}')


async def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token
    application = Application.builder().token(BOT).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    #application.add_handler(MessageHandler(TEXT, echo))
    application.add_handler(MessageHandler(TEXT, flomo))

    # log all errors
    application.add_error_handler(error)

    # Start the Bot using run_polling() method
    # 在v20+版本中，run_polling()替代了之前的initialize()+start_polling()+idle()组合
    application.run_polling()
    
    # run_polling()方法会自动处理Ctrl-C和SIGINT等信号，非阻塞并优雅地停止机器人


if __name__ == '__main__':
    main()
