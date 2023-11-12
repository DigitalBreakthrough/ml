from config import TOKEN
from telegram import ForceReply, Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardMarkup, ReplyKeyboardRemove, Bot
from telegram.ext import Application, Updater, CommandHandler, CallbackContext, MessageHandler, filters, \
    CallbackQueryHandler
from db import db_session
from db.user import User

db_session.global_init("db/users.db")

keyboard = [

    [
        KeyboardButton('/help'),
        KeyboardButton('/Subscrabe'),
        KeyboardButton('/UnSubscrabe'),
    ]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_html(
        rf"""Здравствйте, {update.effective_user.mention_html()}!
Этот бот отправляет вам данные, когда на производстве случается опасная ситуация
Чтобы подписаться на события - /Subscrabe
Чтобы отписатьяс от события - /UnSubscrabe""",
        reply_markup=reply_markup
    )


async def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("""Чтобы подписаться на события - /Subscrabe
Чтобы отписатьяс от события - /UnSubscrabe""")


async def subsc(update: Update, context: CallbackContext) -> None:
    session = db_session.create_session()
    user = User(
        chat_id=update.message.chat_id
    )
    session.add(user)
    session.commit()
    await update.message.reply_text("Вы подписались", reply_markup=reply_markup)


async def cancel(update: Update, context: CallbackContext) -> None:
    session = db_session.create_session()
    user = session.query(User).filter(User.chat_id == update.message.chat_id).first()
    if user:
        session.delete(user)
        session.commit()
    await update.message.reply_text("Вы отписались", reply_markup=reply_markup)


def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("Help", help_command))
    application.add_handler(CommandHandler("Subscrabe", subsc))
    application.add_handler(CommandHandler("UnSubscrabe", cancel))
    application.run_polling()


if __name__ == "__main__":
    main()
