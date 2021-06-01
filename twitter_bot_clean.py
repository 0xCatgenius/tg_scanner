import tweepy
import datetime
import json
import os
import logging
import pickle
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

PORT = int(os.environ.get('PORT', 3978))

# Authenticate to Twitter
auth = tweepy.OAuthHandler("XXX", 
    "XXX")
auth.set_access_token("XXX", 
    "XXX")

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")



user_list = ['fomosaurus','hotnewcrypto','Rager','unihax0r4000','Fiskantes', 'Rafi_0x','cryptodetweiler', 'hardwood_', 'Crypto_Alita']
# user = api.get_user("fomosaurus")
# print("Last 20 Friends:")
## created_at The UTC datetime that the user account was created on Twitter. Example:

save_json = "ape.json"
def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def get_latest_follow(before_update,after_update,name,current_time):
    value = { k : after_update[k] for k in set(after_update) - set(before_update) }
    current_time = current_time.strftime("%d-%m-%Y %H:%M:%S")
    value = { k : v for k,v in value.items() if current_time == v.get('date_added')}
    if value:
        msg = [name+" has these new following"]
        ##_name following
        ##@XX
        for k,v in value.items():
            acc_create = v.get('created_at')
            url = f'https://twitter.com/{k}'
            new_msg = '@'+str(k)+' Account created:' + str(acc_create) + ' ' + str(url) + '\n'
            msg.append(new_msg)
        x = "\n".join(msg)
        return x
    else:
        return f"{name} has no new following"

def create_records(_name):
    before_update = {}
    user = api.get_user(screen_name=_name, count=5)
    with open(save_json, "r") as json_file:
        dict_1 = json.load(json_file)

    before_update = dict_1.copy()
    print("Current records count:"+ str(len(before_update)))
    now = datetime.datetime.now()
    # print(type(before_update))
    # print(dict_1)
    # print(dict_1.get("DeCusIo"))
    ## filter date before 2021-01-01 
    for follower in user.friends():
        if str(follower.created_at) >= '2021-01-01': 
            dict_1[follower.screen_name] = {
                'followed_by':_name,
                'screen_name':follower.screen_name,
                'created_at':follower.created_at,
                'date_added':now.strftime("%d-%m-%Y %H:%M:%S")   
            }
    print("End records count:"+ str(len(dict_1)))
    if len(before_update) != len(dict_1):
        message = get_latest_follow(before_update,dict_1,_name,now)
    else:
        message = f"{_name} has no new following"
    a_file = open(save_json, "w")
    json.dump(dict_1, a_file, default = myconverter)
    a_file.close()  
    return message




    ## >= query time
# for u in user_list:
#     print('Collecting...'+str(u))
#     create_records(u)

# get_latest_follow()


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = 'XXX'

chn_id ='XXX'
base_url = 'https://api.telegram.org/bot1687584692:AAEn0VK5kOd8nl8tlCI8JLy_snbc11LtB_U/sendMessage?'

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def add(update, context):
    """Send a message when the command /help is issued."""
    # user_list
    outfile = open("user.pk",'r+b')
    user_list = pickle.load(outfile)
    msg = update.message.text
    user = msg.split('@')[1]
    print("Current No. of Users: "+ str(len(user_list)))
    user_list.append(user)
    print("After No. of Users: "+ str(len(user_list)))
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Added {user}\n Current List {user_list}")

    pickle.dump(user_list,outfile)
    outfile.close()


# def callback_alarm(context: CallbackContext):
#     bot.send_message(chat_id=update.effective_chat.id, text='Hi, This is a the current update')

# def repeat(update, context):
#     for u in user_list:
#         print('Collecting...'+str(u))
#         msg = create_records(u)
#         context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

def new(update, context):
    """Echo the user message."""
    # infile = open("user.pk",'rb')
    # user_list = pickle.load(infile)
    # infile.close()
    for u in user_list:
        print('Collecting...'+str(u))
        msg = create_records(u)
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
        # update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

          
def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)
    

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    # dp.add_handler(CommandHandler("add", add))
    dp.add_handler(CommandHandler("new", new))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, new))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url='https://fierce-shore-25584.herokuapp.com/' + TOKEN)
    updater.bot.setWebhook('https://fierce-shore-25584.herokuapp.com/' + TOKEN)

    # Start the Bot
    # updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()