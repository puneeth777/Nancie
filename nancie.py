import asyncio
from datetime import datetime

import emoji
from telegram import Update, constants
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, ApplicationHandlerStop, TypeHandler

from src.brain import Brain
from src.config import Config
from src.init import init_nancie
from src.utils import get_base_format


async def process_message_queue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for user_id, user_state in context.user_states.items():
        message_queue = user_state['message_queue']
        print(len(message_queue))
        if len(message_queue) > 0:
            message = message_queue.pop(0)
            print(message)
            response = Brain().execute(message['message'], message['name'])
            print(response)
            await update.message.reply_text(text=response, parse_mode=constants.ParseMode.HTML)


async def whitelist_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id not in Config().get_allowed_users() or update.message.chat.type != 'private':
        await update.effective_message.reply_text(f"Hey {update.message.chat.first_name}! You are not allowed to use "
                                                  f"me YET!",
                                                  reply_to_message_id=update.message.message_id)
        raise ApplicationHandlerStop


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender = update.message.from_user
    user_states = context.user_states
    if sender.id not in user_states:
        sender = update.message.from_user
        context.user_states[sender.id] = get_base_format()
    message = update.message.text
    message = emoji.replace_emoji(message, replace='').strip()
    if not message:
        return
    message_queue = user_states[sender.id]['message_queue']
    if len(message_queue) > 0:
        await update.message.reply_text('<i>Nancie is typing, please be patient</i>',
                                        parse_mode=constants.ParseMode.HTML)
    else:
        message_queue.append({
            'name': sender.full_name,
            'message': message,
            'dateTime': datetime.now()
        })
        await process_message_queue(update, context)


def run_telebot():
    app = ApplicationBuilder().token(Config().get_telegram_bot()).build()

    filters_users = TypeHandler(Update, whitelist_users)
    app.add_handler(filters_users, -1)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)

    handlers = [message_handler]
    for handler in handlers:
        app.add_handler(handler)

    user_states = {}
    app.context_types.context.user_states = user_states
    print("Nancie is online..")
    app.run_polling()


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # no need in Linux
    init_nancie()
    run_telebot()
