
import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def message(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    import requests
    from bs4 import BeautifulSoup
    URL = 'https://asaxiy.uz/product?key=telefon'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")  
    # print(soup.prettify()) 
    for i in range(0,10):
        title = soup.find_all("h5", class_="product__item__info-title")[i].text
        # print(title.text)
        content = str(soup.find_all("span", class_="product__item-price")[i].text)
        image = soup.find_all("div", class_="product__item-img")[i].find_all("img")[0]
        size = len(image["data-src"])
        if image['data-src'][size - 5:] == ".webp":
            image_url = image['data-src'][:size - 5]
        else:
            image_url = image['data-src']

        # print(image['data-src'][:size - 5])
        # update.message.reply_photo(photo="https://assets.asaxiy.uz/product/main_image/desktop//621b526ce2cbf.jpg")
        update.message.reply_photo(image_url,f"{title}\n\nprice: {content}")

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5470778624:AAHzp7Vp9Kod3wgFkvreaGDx7PqWnogM1ko")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()