import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import AutoSearcherFunction

url = 'https://www.ebay.it/sch/i.html?_from=R40&_nkw=iPhone+12+256GB&_in_kw=3&_ex_kw=mini+pro+max+32GB+64GB+128GB+512GB+1TB+scheda+ricambi+cover+protezione+rotto+batteria+custodia&_sacat=0&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=39100&_sargn=-1%%26saslc%%3D1&_salic=101&_sop=1&_dmd=1&_ipg=60&LH_Sold=1&rt=nc'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Auto eBay is a bot that send you the eBay research for your current AutoSearcher program :)"
        )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text
        )

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text_caps
        )

async def average(update: Update, context : ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=AutoSearcherFunction.items_price_average(url)
    )


#Da lasciare per ultimo
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command :("
        )

if __name__ == '__main__':
    application = ApplicationBuilder().token('5222921867:AAFzL-IV4o1CU8C2Ncgea3yQO3VRREtGfwo').build()
    
    info_handler = CommandHandler('info', info)
    #Si possono aggiungere filtri personalizzati (cerca AdvancedFilters)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)
    average_handler = CommandHandler('average', average)
    #Da lasciare per ultimo 
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(info_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(average_handler)
    #Da lasciare per ultimo 
    application.add_handler(unknown_handler)
    
    
    application.run_polling()