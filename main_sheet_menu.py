#!/usr/bin/python
# -*- coding: utf-8 -*-

# NKN Bot using Google Docs 
# 2018.6.6 by Shunda, Long Wang

import time
import pygsheets
import logging
import threading
import re
from telebot import *
from hash import *
from config import TOKEN, SHEET_KEY, SERVICE_FILE, MONITOR_GROUPS, OUTH_FILE
import requests

from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


#initilizing lock, logger and google sheet
LANG = 'EN'
lock = threading.Lock()
logger.setLevel(logging.INFO)
gc = pygsheets.authorize(outh_file=OUTH_FILE)
sh = gc.open('NKNbot') # Open spreadsheet and then workseet

# <Worksheet '新加群名单' index:1>
# <Worksheet '接受奖励地址' index:2>
# <Worksheet '邀请数量统计' index:3>
reply_wks = sh.sheet1 # reply sheet
new_members_wks = sh.worksheet(value=1) # record new group members
addr_wks= sh.worksheet(value=2) # record reward addresses
invite_wks = sh.worksheet(value=3) # count invite number 

#import Keyboards methods
from keyBoards import *
from common import *
from menuMessages import *

############################### menu event handler ############################################
def start(bot, update):
  update.message.reply_text(main_menu_message(),
                            reply_markup=main_menu_keyboard())

def start1(bot, update):
  update.message.reply_text(main_menu_message_CN(),
                            reply_markup=main_menu_keyboard_CN())
            
def main_menu(bot, update):
  query = update.callback_query
  bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=main_menu_message(),
                        reply_markup=main_menu_keyboard())

def main_menu_CN(bot, update):
    query = update.callback_query
    bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=main_menu_message_CN(),
                        reply_markup=main_menu_keyboard_CN())
  
def join_menu(bot, update):
    query = update.callback_query
    bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=joinNKN_menu_message(),
                        reply_markup=back_menu_keyboard())

def join_menu_CN(bot, update):
    query = update.callback_query
    bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=joinNKN_menu_message(),
                        reply_markup=back_menu_keyboard_CN())
                        
def doc_menu(bot, update):
    try:
        logger.info('/doc')
        reply = getValue('/doc')
        if reply != "":
            query = update.callback_query
            bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=reply,
                        reply_markup=back_menu_keyboard())
    except Exception as e:
        logger.error('/doc ERROR: %s', e)

def doc_menu_CN(bot, update):
    try:
        logger.info('User requesting /doc_CN')
        reply = """NKN 文档:
        📖NKN白皮书: t.me/nknorg/43545
        📖NKN 经济模型, 路线图: t.me/nknorg/35053
        📖令牌信息: t.me/nknorg/35056
        📖AMA 2018年4月: t.me/nknorg/43548

        视频:
        AMA: https://www.youtube.com/watch?v=u7K0NeTeB3M&t=129s
        NEO Global Capital had shared about NKN: https://youtu.be/_yQGHFIaqhg?t=15m35s
        NKN interview by Boxmining: https://www.youtube.com/watch?v=o95Uu4m_hXw&feature=youtu.be
        Short video on NKN introduction by Boxmining: https://www.youtube.com/watch?v=aFR9k8IPEdw&feature=youtu.be
        Live interview with Ivan on tech: https://t.co/Ch6kN0M3e4
        Testnet preview demo: https://www.youtube.com/watch?v=0Kluy9YjTVI&feature=youtu.be"""
        if reply != "":
            query = update.callback_query
            bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=reply,
                        reply_markup=back_menu_keyboard_CN())
    except Exception as e:
        logger.error('/doc ERROR: %s', e)

def myAccount_menu(bot, update):
    try:
        logger.info('/myAccount')
        #query = vars(update.callback_query)
        logger.info(update.callback_query.from_user)
        query = update.callback_query
        from_user = update.callback_query.from_user
        account = getAccount(from_user.id) 
        if account == -1:
            reply = "You haven't join NKN group."
        else:
            points = getPoints(bot, from_user)
            reply = "Hello %s\nYou invited %s friends\nYou have %s points" %(account[0], account[1],points)
        bot.edit_message_text(chat_id=query.message.chat_id,
                    message_id=query.message.message_id,
                    text=reply,
                    reply_markup=back_menu_keyboard())
    except Exception as e:
        logger.error('/myAccount ERROR: %s', e)
        
def myAccount_menu_CN(bot, update):
    try:
        logger.info('/myAccount')
        #query = vars(update.callback_query)
        logger.info(update.callback_query.from_user)
        query = update.callback_query
        from_user = update.callback_query.from_user
        account = getAccount(from_user.id) 
        if account == -1:
            reply = "你还没有加入NKN群"
        else:
            points = getPoints(bot, from_user)
            reply = u"您好 %s\n您目前已经邀请了 %s 位朋友\n你现在一共有 %s 分" %(account[0], account[1],points)
        bot.edit_message_text(chat_id=query.message.chat_id,
                    message_id=query.message.message_id,
                    text=reply,
                    reply_markup=back_menu_keyboard_CN())
    except Exception as e:
        logger.error('/myAccount ERROR: %s', e)

def lang_menu(bot, update):
    try:
        logger.info('/language')
        query = update.callback_query
        logger.info(query.message.from_user)
        bot.edit_message_text(chat_id=query.message.chat_id,
                    message_id=query.message.message_id,
                    text='Choose your language',
                    reply_markup=language_menu_keyboard())
    except Exception as e:
        logger.error('/language ERROR: %s', e)

def en_menu(bot, update):
    try:
        logger.info('set language to engilsh')
        query = update.callback_query
        logger.info(query.message.from_user)
        bot.edit_message_text(chat_id=query.message.chat_id,
                    message_id=query.message.message_id,
                    text=main_menu_message(),
                    reply_markup=main_menu_keyboard())
    except Exception as e:
        logger.error('/engilsh ERROR: %s', e)

def cn_menu(bot, update):
    try:
        logger.info('Set language to chinese')
        query = update.callback_query
        logger.info(query.message.from_user)
        bot.edit_message_text(chat_id=query.message.chat_id,
                    message_id=query.message.message_id,
                    text=main_menu_message_CN(),
                    reply_markup=main_menu_keyboard_CN())
    except Exception as e:
        logger.error('/chinese ERROR: %s', e)

def reward_addr(bot, update):
    check_reward_addr(update.message)
# /reward_addr : check current reward address
def check_reward_addr(message):
    try:
        #two ways get value from worksheet
        #invite_wks.get_value((row, col))   this will get error when the cell is empty
        #invite_wks[row-1][col]    for this method row has to minus one to get the right record, because array started at 0
        #addr = invite_wks.get_value((row, 8))
        #logger.info(addr)
        row = findKey(invite_wks, str(message.from_user.id))
        logger.info(row)
        addr = invite_wks[row-1][7]
        logger.info(addr)
        
        if row == -1:
            logger.info(row)
            en_reply = "You haven't join the program yet."
            cn_reply = u"您还没有加入积分项目，请先注册"
            reply_two_languages(message, en_reply, cn_reply)

        if addr != "":
            en_reply = "Your current reward address is %s\nIf you want to change the address, you can reply a new address to the bot." % addr
            cn_reply = u"当前设置的接受奖励的钱包地址为: %s\n如果你想更换钱包地址，可以给机器人回复一个新的地址" % addr 
            reply_two_languages(message, en_reply, cn_reply)
        else:
            en_reply = "You haven't set your reward address yet. You can reply your wallet address to the bot to set it."
            cn_reply = "你还未设置用于接受奖励的钱包地址，你可以通过给机器人发送钱包地址来进行设置"
            reply_two_languages(message, en_reply, cn_reply)
    except Exception as e:
        logger.error('get reward address ERROR: %s', e)

def refer_menu(bot, update):
    try:
        lock.acquire()
        logger.info('/invite')
        logger.info(update.callback_query.message.chat)
        from_user = update.callback_query.message.chat
        code = generateInviteCode("NKN", from_user.id)
        count = getInviteCount(str(from_user.id))
        #when invite count is empty, we create a new user in invite worksheet
        if count == "":
            values = [
                from_user.username,
                from_user.first_name,
                from_user.last_name,
                from_user.id,
                code, 
                0
            ]
            insertRow(invite_wks, values)
            count = "0"
        
    except Exception as e:
        logger.error('/invite ERROR: %s', e)
    finally:
        lock.release()
    query = update.callback_query
    bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=refer_menu_message(code, count),
                        reply_markup=back_menu_keyboard())

def refer_menu_CN(bot, update):
    try:
        lock.acquire()
        logger.info('/invite')
        logger.info(update.callback_query.message.chat)
        from_user = update.callback_query.message.chat
        code = generateInviteCode("NKN", from_user.id)
        count = getInviteCount(str(from_user.id))
        #when invite count is empty, we create a new user in invite worksheet
        if count == "":
            values = [
                from_user.username,
                from_user.first_name,
                from_user.last_name,
                from_user.id,
                code, 
                0
            ]
            insertRow(invite_wks, values)
            count = "0"
        
    except Exception as e:
        logger.error('/invite ERROR: %s', e)
    finally:
        lock.release()
    query = update.callback_query
    bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=refer_menu_message_CN(code, count),
                        reply_markup=back_menu_keyboard_CN())
    
# @bot.message_handler(commands=['faq'])
# def send_faq(message):
#     try:
#         logger.info('/faq')
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         reply = "Questions list:\n"
#         faq_list = getFaqList()
#         for question in faq_list:
#             itembtn = types.KeyboardButton(question)
#             markup.add(itembtn)
#             reply = reply + "\n" + question
#         bot.send_message(message.chat.id, reply, reply_markup=markup)
#     except Exception as e:
#         logger.error('/faq ERROR: %s', e)

def record_new_members(bot, update):
    logger.info(update.message)
    message = update.message
    try:
        if message.chat.title in MONITOR_GROUPS:
            logger.info('new member joined')
            for member in message.new_chat_members:
                try:
                    lock.acquire()
                    logger.info(member)
                    if findKey(new_members_wks, str(member.id)) == -1: # avoid recording users that have already existed
                        # code = ""
                        # if message.from_user.id != member.id:  # someone invites a new member
                        #     from_user = message.from_user
                        #     logger.info(from_user)
                        #     code = generateInviteCode("NKN", from_user.id)
                        #     if addInviteCount(code) == -1: # inviter hasn't registered yet
                        #         from_user_info = [
                        #             from_user.username,
                        #             from_user.first_name,
                        #             from_user.last_name,
                        #             from_user.id,
                        #             code, 
                        #             1
                        #         ]
                        #         insertRow(invite_wks, from_user_info) # register inviter
                        new_member_info = [
                            json_serial(message.date),
                            member.username, 
                            member.first_name,
                            member.id,
                            ""
                        ]
                        insertRow(new_members_wks, new_member_info) # record new member's infomation
                except Exception as e:
                    raise
                finally:
                    lock.release()
    except Exception as e:
        logger.error('record new members ERROR: %s', e)

def echo(bot, update):
    try:
        logger.info(update)
        reply = getValue(update.text)
        if reply != "":
            update.message.reply_text(reply)
    except Exception as e:
        logger.error('handler message ERROR: %s', e)

def findUser(wks, key):
    cell_list =wks.find(key)
    #not find, new user
    if len(cell_list) == 0:
        return 1
    else:
        return -1

def findKey(wks, key):
    # pattern = re.compile("^" + key, re.I) # ignore case
    # cell_list = wks.find(pattern)
    cell_list = wks.find(key)
    if len(cell_list) == 0:
        return -1
    else:
        return cell_list[0].row

def insertRow(wks, values, end_flag='--END--'):
    row = findKey(wks, end_flag)
    if row != -1:
        wks.insert_rows(row-1, values=values)

def checkCodeExistence(code):
    print(code)
    row = findKey(invite_wks, code)
    print(row)
    
    row = invite_wks.find(code)
    print(row)
    if len(row) != 0:
        return False
    else:
        return True

def addInviteCount(code):
    row = findKey(invite_wks, code)
    if row != -1:
        count = invite_wks[row-1][5]
        count = int(count) + 1  
        invite_wks.update_cell((row, 6), count)
        return count
    else:
        return -1

def getInviteCount(key):
    row = findKey(invite_wks, key)
    if row != -1:
        return invite_wks[row-1][5] # 第六列作为回复
    else:
        return ""

# find user info based on user id
def getAccount(key):
    print(key)
    row = findKey(invite_wks, str(key))
    print(row)
    if row != -1:
        # return reply_wks[row-1][0]
        return [invite_wks.get_value((row, 1)), invite_wks.get_value((row, 6))] # 第一和六列作为回复
    else:
        return -1

# find the corresponding reply in google doc by given key word
def getValue(key):
    row = findKey(reply_wks, key)
    if row != -1:
        # return reply_wks[row-1][0]
        return reply_wks.get_value((row, 1)) # 第一列作为回复
    else:
        return ""

def getFaqList():
    # find faq questions
    faq_filter = re.compile(r'^Q\d+\..')
    cell_list = reply_wks.find(faq_filter)
    faq_list = []
    for question in cell_list:
        faq_list.append(question.value)
    return faq_list

def getPoints(bot, from_user):
    points = 0
    #check if user is in new invited list
    #find will return an array contains cell qulify the key
    #findKey will return the row number
    #arr = new_members_wks.find(str(from_user.id))
    row = findKey(new_members_wks, str(from_user.id))
    logger.info("Get points for user on row %s" %row)
    if row != -1:
        ref = new_members_wks[row-1][4]
        logger.info("User's refer code:%s" %ref)
        if ref != "":
            points = points + 100
    
    #get user invite count
    #arr = invite_wks.find(str(from_user.id))
    row = findKey(invite_wks, str(from_user.id))
    if row != -1:
        count = invite_wks[row-1][5]
        logger.info("User invited %s friends" %count)
        if count != '':
            points = points + 100*int(count)
    invite_wks.update_cell((row, 7), points)
    return points

#################command, message handler functions#######################################
def echoMessageHandler(bot, update):
    logger.info(update.message.text)
    #if user typed in NKN code
    msg = update.message.text
    pattern = re.compile("^NKN[A-F0-9]{5}")
    addrPattern = re.compile("[A-Za-z0-9]{34}")
    if pattern.match(msg):
        handle_invite_code(update.message)
        #update.message.reply_text("code...")
    if addrPattern.match(msg):
        handle_reward_addr(update.message)

def handle_invite_code(message):
    try:
        logger.info('invite code')
        #check if the code exist
        if checkCodeExistence(message.text):
            logger.info("The invite code doesn't exist.")
            reply_two_languages(message, "The invite code doesn't exist.", "邀请码不存在")
            return 
        #check if user's code is matching his own code
        code = generateInviteCode("NKN", message.chat.id)
        if code == message.text:
            logger.info("You can't use your own invite code.")
            reply_two_languages(message, "You can't use your own invite code.", "你不能使用自己的邀请码")
            return
        try:
            lock.acquire()
            #check if user already exists in our db
            exist = findUser(new_members_wks, str(message.chat.id))
            if exist == 1:
                #new user, need to create new account, insert to new_members_wks
                new_member_info = [
                        json_serial(message.date), 
                        message.chat.username, 
                        message.chat.first_name,
                        message.chat.id,
                        message.text
                ]
                insertRow(new_members_wks, new_member_info) 
                #add invite count for inviter
                addInviteCount(message.text)
                # row = findKey(invite_wks, message.text)
                # invite_wks.update_cell((row, 5), message.text)
                logger.info(str(message.chat.id) + ":" + message.text)
                reply_two_languages(message, 
                    "The code is used successfully!\nIf you haven't set your reward address, you can reply your wallet address to the bot. Candies will be sent to the address after the activity.", 
                    "邀请码使用成功!\n积分可以兑换糖果哦，如果您还没有绑定NEO钱包，可以给机器人回复您的钱包地址进行设置，活动结束后奖励会发送到对应的地址"
                )
            else:
                logger.info("You aren't a new member of NKN group.")
                reply_two_languages(message, "You aren't a new member of NKN group.", "你不是一个新加群的用户, 无法使用邀请码")
        except Exception as e:
            raise
        finally:
            lock.release()
    except Exception as e:
        logger.error('use invite code ERROR: %s', e)

# # handle reward address
# @bot.message_handler(regexp="^A[A-Za-z0-9]{34}")	
def handle_reward_addr(message):
    try:
        lock.acquire()
        #convert object ot dict
        #message = vars(message)
        logger.info(message.from_user)
        from_user = message.from_user
        row = findKey(invite_wks, str(from_user.id))
        if row != -1:
            invite_wks.update_cell((row, 8), message.text)
            message.reply_text("Reward address is set successfully!\nYou can type /reward_addr to check your current reward address.")
        # reply_two_languages(message, 
        #     "Reward address is set successfully!\nYou can type /reward_addr to check your current reward address.", 
        #     "接受奖励的钱包地址设置成功!\n你可以输入 /reward_addr 来查看当前设置的地址"
        # )
        else:
            # addr_info = [
            #     from_user.username,
            #     from_user.first_name,
            #     from_user.last_name,
            #     from_user.id,
            #     message.text
            # ]
            # insertRow(addr_wks, addr_info)
            message.reply_text("Please register the program first")
    except Exception as e:
        logger.error('set reward address ERROR: %s', e)
    finally:
        lock.release()

#get points from /points
def points(bot, update):
    update.message.reply_text(getPoints(bot, update.message.from_user))
############################# App entry #########################################
def main():
    """Start the bot."""
    # Create the EventHandler and pass it with bot's token.
    updater = Updater(TOKEN)
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('start1', start1))
    dp.add_handler(CommandHandler('points', points))
    dp.add_handler(CommandHandler('reward_addr', reward_addr))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echoMessageHandler))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, record_new_members))

    # menu handler
    
    dp.add_handler(CallbackQueryHandler(main_menu_CN, pattern='mainCN'))
    dp.add_handler(CallbackQueryHandler(join_menu_CN, pattern='joinNKNCN'))
    dp.add_handler(CallbackQueryHandler(refer_menu_CN, pattern='referCN'))
    dp.add_handler(CallbackQueryHandler(doc_menu_CN, pattern='docCN'))
    dp.add_handler(CallbackQueryHandler(myAccount_menu_CN, pattern='myAccountCN'))

    dp.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    dp.add_handler(CallbackQueryHandler(join_menu, pattern='joinNKN'))
    dp.add_handler(CallbackQueryHandler(refer_menu, pattern='refer'))
    dp.add_handler(CallbackQueryHandler(doc_menu, pattern='doc'))
    dp.add_handler(CallbackQueryHandler(myAccount_menu, pattern='myAccount')) 


    dp.add_handler(CallbackQueryHandler(lang_menu, pattern='Lang')) 
    dp.add_handler(CallbackQueryHandler(en_menu, pattern='EN')) 
    dp.add_handler(CallbackQueryHandler(cn_menu, pattern='CN')) 
    
    

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()