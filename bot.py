import logging
import os
import re
import random
from dotenv import load_dotenv

from telegram.ext import Updater, MessageHandler, Filters

PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
load_dotenv()
TOKEN = os.environ.get('TOKEN')


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def processMsg(msg, first_name):
    if "slay" in msg:
        return "SLAYY"
    elif "neslo" in msg:
        return "Did someone say neslo??"
    # elif "noyouare" in msg:
    #     return "CORRECT"
    # elif ("iam" in msg) or ("im" in msg):
    #     if first_name not in msg:
    #         return f"no you are {first_name}"
    #     return "no you are not"
    elif ("think about it" in msg) or ("think abt it" in msg):
        return f"ya {first_name} just think about it okay just think about it"
    elif "rome" in msg:
        return "bless your GI tract"
    elif ("code" in msg) or ("coding" in msg):
        return "who opened this pandora's box"
    elif ("deez nuts" in msg) or ("deeznuts" in msg):
        return "viva la deez nuts"
    elif ("christmas" in msg) or ("xmas" in msg):
        return "MERRY CHRISTMAS SLEIGHH"
    elif "meow" in msg:
        return "MEOWWWW"
    else:
        return ""


def processAnnabelle(msg):
    if "slay" in msg:
        return "yas annabelle SLAY"
    elif "think" in msg:
        return "ya annabelle just think about it okay just think about it"
    else:
        return ""


def msgPreprocessor(msg):
    result = msg.lower()
    specialChars = "[^A-Za-z0-9 ]+"
    result = re.sub(specialChars, "", result)
    resultWithoutSpaces = re.sub(" ", "", result)
    slay_pattern = "[S,s]+[L,l]+[A,a]+[Y,y]"
    slay_result = re.match(slay_pattern, resultWithoutSpaces)
    meow_pattern = "[M,m]+[E,e]+[O,o]+[W,w]"
    meow_result = re.match(meow_pattern, resultWithoutSpaces)
    if slay_result:
        return "slay"
    if meow_result:
        return "meow"
    return result


def codePreprocessor(msg):
    keywords = ["{", "}", "(", ")", ";", "return", "int", "char", "print", "if", "else", "while", "for", "=", "hello world"]
    length = len(keywords)
    count = 0
    for i in keywords:
        if i in msg:
            count += 1
    percentageCode = count / length
    if percentageCode > 0.25:
        return "who opened this pandora's box"
    return ""


def reply(update, context):
    user_id = update.message.from_user.username
    user_name = update.message.from_user.first_name.lower()

    a = random.randint(0, 100)
    if a == 14:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="hehehehheheheheh"
        )

    codeReply = codePreprocessor(update.message.text)
    if codeReply != "":
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=codeReply
        )
        return

    msg = msgPreprocessor(update.message.text)
    reply_text = ""
    if user_id == "annxbellee":
        reply_text = processAnnabelle(msg)
    if reply_text == "":
        reply_text = processMsg(msg, user_name)
    if reply_text != "":
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=reply_text
        )


def main():
    """Start the bot."""
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(MessageHandler(Filters.text and (~Filters.command), reply))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://annabelle-bot.herokuapp.com/' + TOKEN)
    # updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
