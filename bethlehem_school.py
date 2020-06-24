from telegram.ext import (
        Updater, 
        CommandHandler, 
        MessageHandler, 
        Filters,
        CallbackQueryHandler
    )
# from googlemaps import Client as GoogleMaps
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import os
import logging
import requests
import nltk
import io
import numpy as np
import random
import string
import warnings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
 

# # Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

reply_keyboard = [
                    ['/start', '/info', '/quiz', '/joke'],
                    ['/physics', '/channel', '/clear', '/first']
                ]
markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

# update.message.reply_text('Bye! Hope to see you again next time.',
#                               reply_markup=ReplyKeyboardRemove())

# def start(update, context):
#     print("starting...")
#     update.message.reply_text("To continue press\n /{}".format(info(update, context)), reply_markup=markup)

def start(update, context):
    msg_get = update.message
    context.user_data['username']= msg_get.from_user.first_name
    data = context.user_data['username']
    data = "{}".format(data)
    data = str(data)
    text = '''
    Hi {} Welcome to /Bethlehem /Secondary /School /Chat /Bot. I am an /Intelligent /Robot. You can press the /links or the /buttons below to access the /resource that I have. You can also type any link on your /message /box to access me. for example when you type /quiz in your message dialog, I will directly takes you to the /quiz and so on. I may not be available unless the /background /software runs on me that helps me to chat with you. Have a good time with me.

    * /start \n  
    * /info  \n  
    * /quiz \n 
    *  visite @bethlehemschool\n 
    * physics  \n
        
    Thanks in advance !!
    contact @: 
    ephremnigussie7@gmail.com
    https://github.com/ephrem601/
    https://twitter.com/@EphremOfficials
    https://m.facebook.com/ephrem.nigussie.125

    '''.format(data)
    update.message.reply_text(text=text, reply_markup=markup)
   
# @bot.message_handler(content_types=['location'])
# def handle_location(message):
#     print("{0}, {1}".format(message.location.latitude, message.location.longitude))

def info(update, context):
    msg = update.message
    context.user_data['text']=msg.text
    context.user_data['firstname']=msg.from_user.first_name
    firstname=context.user_data['firstname']
    chatId= msg.chat_id
    data = 'Welcome /'+firstname+' \nYour Chat ID is /'+str(chatId) 
    
    data = str(data)
    update.message.reply_text(data)
     
    #update.message.reply_text(data) 


def quiz_test(update, context):
    return update.message.reply_text("Please Select a subject\n for physics t.me/QuizBot?start=RWN3JIKR")
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Similarity search NLTK Learn
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey")
GREETING_RESPONSES = ["hi", "hey", "*node*", "hello", "I am glad", "you are talking to me"]

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            # return random.choice(GREETING_RESPONSES) returns chices randomly
            return GREETING_RESPONSES



def learn_physics(update, context):
    print("starting physics lesson...")
    msg = update.message
    context.user_data['text']=msg.text
     
    context.user_data['username']=msg.from_user.first_name
    # username=context.user_data['username']
    warnings.filterwarnings('ignore')
    f=open('physics.txt','r', errors='ignore')
    raw=f.read()
    raw=raw.lower()#convert to lowercase
    sent_tokens=nltk.sent_tokenize(raw) #convert to list of sentences
    # word_tokens=nltk.word_tokenize(raw)#convert to list of words
    lammer=nltk.stem.WordNetLemmatizer()

    def lemmatizeToken(tokens):
        return [lammer.lemmatize(token) for token in tokens]
    remove_punct_dict = dict((ord(punct), None)for punct in string.punctuation)

    def lematizeNormalize(text):
        return lemmatizeToken(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

    def response(user_response):
    
        chatbot_response =''
        sent_tokens.append(user_response)
        TfidfVec = TfidfVectorizer(tokenizer=lematizeNormalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(sent_tokens)
        vals  = np.array(cosine_similarity(tfidf[-1], tfidf))
        
        idx = np.argsort(vals)
        idx = idx[0][-2] 
        flat = vals.flatten()
        flat = np.array(flat)
        flat = np.sort(flat)
        
        req_tfidf = flat[-1]
        if req_tfidf==0:
            chatbot_response = chatbot_response+"I am sorry! I don't unserstand you"

        else:
            chatbot_response = chatbot_response+sent_tokens[idx]
            
            return chatbot_response

    flag = True
    
    if flag==True:
        
        user_response = context.user_data['text']
        user_response = user_response.lower()
        
        if user_response !='bye':
        
            if user_response=='thanks' or user_response=='thank you':
                flag = False
                print("Chatbot: you are welcome")
            
            else:
                if greeting(user_response)!=None:
                    update.message.reply_text("Chatbot: \n"+greeting(user_response))
                else: 
                    response_to_telegram_console =response(user_response)
                    response_to_telegram_console = str(response_to_telegram_console)  
                    update.message.reply_text(response_to_telegram_console)
                    print("Definition: \n",response(user_response))
                    sent_tokens.remove(user_response)
            
        else:
            flag = False
            print("Chatbot : Bye! take care..")

 
def main():
    print("Running...")
    bot_token = "1187308654:AAE2JsgFgVudYpk_V_wR6jxbuX_ik8mdQuI"
     
    updater = Updater(bot_token, use_context=True)
    # a dispatcher disconnects from the server
    
    dp = updater.dispatcher

    # Get the dispatcher to register to handler
    dp.add_handler(CommandHandler('start', start, pass_user_data=True))
    dp.add_handler(CommandHandler('info', info))
    dp.add_handler(CommandHandler('quiz',quiz_test))
     
    dp.add_handler(MessageHandler(Filters.text, learn_physics))
    
    updater.start_polling()

      

     
    updater.idle()


if __name__ == '__main__':
    
    main()
