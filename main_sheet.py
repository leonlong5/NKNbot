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
from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

#get user data from current group
import json
USER_DATA_GROUP = {'Name': 'Zara'}
with open('NKNCN.json') as json_data:
    d = json.load(json_data)
    for item in d:
        USER_DATA_GROUP[item['id']] = "0"

with open('NKN.json') as json_data:
    d = json.load(json_data)
    for item in d:
        USER_DATA_GROUP[item['id']] = "0"
#print(395368493 in USER_DATA_GROUP)

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

new_members_wks_thrend = sh.worksheet(value=1)
invite_wks_thrend = sh.worksheet(value=3)

#import Keyboards methods
from keyBoards import *
from common import *
from menuMessages import *

############################### Menu event handler #########################################################################
def start(bot, update, args):
    isbot = update.message.from_user.is_bot
    logger.info(isbot)
    if isbot == True:
        update.message.reply_text("Bot detected!!!")
        return
    userArgs = "".join(args)
    logger.info("User start event, if user is from refer link, code is : %s" %userArgs)
    # if userArgs != "":
    #     message = update.message
    #     message.text = userArgs
    #     handle_invite_code(message)
    update.message.reply_text(main_menu_message(),
                            reply_markup=main_menu_keyboard())

def start1(bot, update):
    update.message.reply_text(main_menu_message_CN(),
                            reply_markup=main_menu_keyboard_CN())
            
# def test(bot, update):
#     key = findKey("new_members_wks", "420459892")
#     code = new_members_wks[21][4]
#     update.message.reply_text("%s %s"%(key, code))

@run_async
def main_menu(bot, update):
  query = update.callback_query
  bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=main_menu_message(),
                        reply_markup=main_menu_keyboard())

@run_async
def main_menu_CN(bot, update):
    query = update.callback_query
    bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=main_menu_message_CN(),
                        reply_markup=main_menu_keyboard_CN())
  
@run_async
def join_menu(bot, update):
    query = update.callback_query
    bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=joinNKN_menu_message(),
                        reply_markup=back_menu_keyboard())

@run_async
def join_menu_CN(bot, update):
    query = update.callback_query
    bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=joinNKN_menu_message(),
                        reply_markup=back_menu_keyboard_CN())
                        
@run_async
def doc_menu(bot, update):
    try:
        logger.info('/doc')
        #reply = getValue('/doc')
        reply = NKN_doc()
        if reply != "":
            query = update.callback_query
            bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=reply,
                        reply_markup=back_menu_keyboard())
    except Exception as e:
        logger.error('/doc ERROR: %s', e)

@run_async
def doc_menu_CN(bot, update):
    try:
        logger.info('User requesting /doc_CN')
        reply = NKN_doc_CN()
        if reply != "":
            query = update.callback_query
            bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=reply,
                        reply_markup=back_menu_keyboard_CN())
    except Exception as e:
        logger.error('/doc ERROR: %s', e)

@run_async
def myAccount_menu(bot, update):
    try:
        logger.info('/myAccount')
        query = update.callback_query
        from_user = query.from_user
        logger.info(from_user)
        gc = pygsheets.authorize(outh_file=OUTH_FILE)
        sh = gc.open('NKNbot') # Open spreadsheet and then workseet
        new_members_wks_thrend = sh.worksheet(value=1)
        invite_wks_thrend = sh.worksheet(value=3)
        #get user invite sheet row number by userID
        cell_list = []
        cell_list = invite_wks_thrend.find(str(from_user.id))
        invite_row_key = -1
        if len(cell_list) != 0:
            invite_row_key = cell_list[0].row
        #get user new memmber sheet row number by userID
        cell_list = []
        cell_list = new_members_wks_thrend.find(str(from_user.id))
        new_member_key = -1
        if len(cell_list) != 0:
            new_member_key = cell_list[0].row
        if invite_row_key == -1 and new_member_key == -1:
            #if not in both sheets, we just give them 0 points
            reply = "Hello %sYou invited 0 friends\nYou have 0 points"%from_user.username
        else:
            logger.info("Get user invite sheet row: %s , new member sheet row: %s" %(invite_row_key, new_member_key))
            #get data
            invite_row_data = []
            new_member_data = []
            invite_count = 0
            if invite_row_key != -1:
                invite_row_data = invite_wks_thrend.get_row(invite_row_key)
                invite_count = invite_row_data[5]
                logger.info("Get user invite sheet row data: %s" %invite_row_data)
            if new_member_key != -1:
                new_member_data = new_members_wks_thrend.get_row(new_member_key)
                logger.info("Get user new member sheet row data: %s" %new_member_data)
            #caculate user points
            points = getPoints(invite_row_data, new_member_data, invite_row_key, invite_wks_thrend)
            reply = u"Hello %s\nYou invited %s friends\nYou have %s points" %(from_user.username, invite_count, points)
        bot.edit_message_text(chat_id=query.message.chat_id,
                    message_id=query.message.message_id,
                    text=reply,
                    reply_markup=back_menu_keyboard())
    except Exception as e:
        logger.error('/myAccount ERROR: %s', e)

@run_async
def myAccount_menu_CN(bot, update):
    try:
        logger.info('/myAccount')
        query = update.callback_query
        from_user = query.from_user
        logger.info(from_user)
        gc = pygsheets.authorize(outh_file=OUTH_FILE)
        sh = gc.open('NKNbot') # Open spreadsheet and then workseet
        new_members_wks_thrend = sh.worksheet(value=1)
        invite_wks_thrend = sh.worksheet(value=3)
        #get user invite sheet row number by userID
        cell_list = []
        cell_list = invite_wks_thrend.find(str(from_user.id))
        invite_row_key = -1
        if len(cell_list) != 0:
            invite_row_key = cell_list[0].row
        #get user new memmber sheet row number by userID
        cell_list = []
        cell_list = new_members_wks_thrend.find(str(from_user.id))
        new_member_key = -1
        if len(cell_list) != 0:
            new_member_key = cell_list[0].row
        if invite_row_key == -1 and new_member_key == -1:
            #if not in both sheets, we just give them 0 points
            reply = "您好 %s\n您目前已经邀请了0位朋友\n你现在一共有0分"%from_user.username
        else:
            logger.info("Get user invite sheet row: %s , new member sheet row: %s" %(invite_row_key, new_member_key))
            #get data
            invite_row_data = []
            new_member_data = []
            invite_count = 0
            if invite_row_key != -1:
                invite_row_data = invite_wks_thrend.get_row(invite_row_key)
                invite_count = invite_row_data[5]
                logger.info("Get user invite sheet row data: %s" %invite_row_data)
            if new_member_key != -1:
                new_member_data = new_members_wks_thrend.get_row(new_member_key)
                logger.info("Get user new member sheet row data: %s" %new_member_data)
            #check if user regestered the program(in the invite count sheet)
            points = getPoints(invite_row_data, new_member_data, invite_row_key, invite_wks_thrend)
            reply = u"您好 %s\n您目前已经邀请了 %s 位朋友\n你现在一共有 %s 分" %(from_user.username, invite_count, points)
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

# def refer_menu(bot, update):
#     try:
#         lock.acquire()
#         from_user = update.callback_query.message.chat
#         code = generateInviteCode("NKN", from_user.id)
#         userKey = findKey('invite_wks', str(from_user.id))
#         logger.info("User %s request refer code:%s "%(from_user.username, code))
#         #when user is not in invite count sheet, we create a new user in invite worksheet
#         if userKey == -1:
#             values = [
#                 from_user.username,
#                 from_user.first_name,
#                 from_user.last_name,
#                 from_user.id,
#                 code, 
#                 0
#             ]
#             insertRow("invite_wks", values)
#     except Exception as e:
#         logger.error('/invite ERROR: %s', e)
#     finally:
#         lock.release()
#     query = update.callback_query
#     bot.edit_message_text(chat_id=query.message.chat_id,
#                                 message_id=query.message.message_id,
#                                 text=refer_menu_message(code),
#                                 reply_markup=back_menu_keyboard())

# def refer_menu_CN(bot, update):
#     try:
#         lock.acquire()
#         from_user = update.callback_query.message.chat
#         code = generateInviteCode("NKN", from_user.id)
#         userKey = findKey('invite_wks', str(from_user.id))
#         logger.info("User %s request refer code:%s "%(from_user.username, code))
#         #when invite count is empty, we create a new user in invite worksheet
#         if userKey == -1:
#             values = [
#                 from_user.username,
#                 from_user.first_name,
#                 from_user.last_name,
#                 from_user.id,
#                 code, 
#                 0
#             ]
#             insertRow("invite_wks", values)
#     except Exception as e:
#         logger.error('/invite ERROR: %s', e)
#     finally:
#         lock.release()
#     query = update.callback_query
#     bot.edit_message_text(chat_id=query.message.chat_id,
#                         message_id=query.message.message_id,
#                         text=refer_menu_message_CN(code),
#                         reply_markup=back_menu_keyboard_CN())


############################ methods help with database search, insert, update ######################################################################
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
    cell_list = []
    if wks == "invite_wks":
        cell_list = invite_wks.find(key)
    if wks == "new_members_wks":
        cell_list = new_members_wks.find(key)
    if wks == "reply_wks":
        cell_list = reply_wks.find(key)
    if wks == "new_members_wks_thrend":
        cell_list = new_members_wks_thrend.find(key)
    if wks == "invite_wks_thrend":
        cell_list = invite_wks_thrend.find(key)
    if len(cell_list) == 0:
        return -1
    else:
        return cell_list[0].row

def insertRow(wks, values, end_flag='--END--'):
    row = findKey(wks, end_flag)
    logger.info("insert row: %s"%row)
    if row != -1:
        if wks == "invite_wks":
            invite_wks.insert_rows(row-1, values=values)
        if wks == "new_members_wks":
            new_members_wks.insert_rows(row-1, values=values)
        if wks == "reply_wks":
            reply_wks.insert_rows(row-1, values=values)
        

def checkCodeExistence(code):
    row = invite_wks.find(code)
    logger.info("Checking code existence %s"%row)
    if len(row) != 0:
        return False
    else:
        return True

def addInviteCount(code):
    row = findKey("invite_wks", code)
    if row != -1:
        rowData = invite_wks.get_row(row)
        count = int(rowData[5])
        logger.info("Get user invite count: %s" %count)
        if count < 30:
            count = count + 1  
            invite_wks.update_cell((row, 6), count)
        return count
    else:
        return -1

# find the corresponding reply in google doc by given key word
def getValue(key):
    row = findKey("reply_wks", key)
    if row != -1:
        # return reply_wks[row-1][0]
        return reply_wks.get_value((row, 1)) # 第一列作为回复
    else:
        return ""

# def getFaqList():
#     # find faq questions
#     faq_filter = re.compile(r'^Q\d+\..')
#     cell_list = reply_wks.find(faq_filter)
#     faq_list = []
#     for question in cell_list:
#         faq_list.append(question.value)
#     return faq_list
def getPoints(invite_row_data, new_member_data, invite_row_key, invite_wks_thrend):
    points = 0
    #check if user used a refer code 
    if new_member_data:
        ref = new_member_data[5]
        logger.info("User verified join group?: %s" %ref)
        if ref != "":
            points = points + 100
    #get user invite count
    if invite_row_data:
        count = invite_row_data[5]
        cur_points = invite_row_data[6]
        if cur_points != "":
            cur_points = int(cur_points)
        else:
            cur_points = 0
        logger.info("User invited %s friends" %count)
        if count != 0:
            points = points + 100*int(count)

        if points != cur_points:
            logger.info("Update points in db if they are not the same %s | %s"%(points, cur_points))
            invite_wks_thrend.update_cell((invite_row_key, 7), points)
    return points

##################################################  command, message handler functions  ###############################################################
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

# def handle_invite_code(message):
#     try:
#         logger.info('invite code: %s'%message.from_user)
#         userID = message.from_user.id
#         #check if user is old user
#         # if userID in USER_DATA_GROUP:
#         #     reply_two_languages(message, "Invalid invitation code. Our record shows you are in our group or you were in the group before.", "邀请码使用无效，我们记录显示你不是我们新群用户")
#         #     return 
#         #check if the code exist
#         if checkCodeExistence(message.text):
#             logger.info("The invite code doesn't exist.")
#             reply_two_languages(message, "The invite code doesn't exist.", "邀请码不存在")
#             return 
#         #check if user's code is matching his own code
#         code = generateInviteCode("NKN", userID)
#         if code == message.text:
#             logger.info("You can't use your own invite code.")
#             reply_two_languages(message, "You can't use your own invite code.", "你不能使用自己的邀请码")
#             return
#         try:
#             lock.acquire()
#             #check if user already exists in our db
#             exist = findKey("new_members_wks", str(userID))
#             if exist == -1:
#                 #new user, need to create new account, insert to new_members_wks
#                 new_member_info = [
#                         json_serial(message.date), 
#                         message.from_user.username, 
#                         message.from_user.first_name,
#                         userID,
#                         message.text
#                 ]
#                 insertRow("new_members_wks", new_member_info) 
#                 # row = findKey(invite_wks, message.text)
#                 # invite_wks.update_cell((row, 5), message.text)
#                 reply_two_languages(message, 
#                     "The code is used successfully! we will verify it after you join NKN group.\nIf you haven't set your reward address, you can reply your wallet address to the bot. Candies will be sent to the address after the activity.", 
#                     "邀请码使用成功! 当你加入NKN群之后，我们会验证。\n积分可以兑换糖果哦，如果您还没有绑定NEO钱包，可以给机器人回复您的钱包地址进行设置，活动结束后奖励会发送到对应的地址"
#                 )
#             else:
#                 logger.info("You aren't a new member of NKN group.")
#                 reply_two_languages(message, "You aren't a new member of NKN group.", "你不是一个新加群的用户, 无法使用邀请码")
#         except Exception as e:
#             raise
#         finally:
#             lock.release()
#     except Exception as e:
#         logger.error('use invite code ERROR: %s', e)

# # handle reward address
# @bot.message_handler(regexp="^A[A-Za-z0-9]{34}")	
def handle_reward_addr(message):
    try:
        lock.acquire()
        logger.info(message.from_user)
        from_user = message.from_user
        row = findKey("invite_wks", str(from_user.id))
        if row != -1:
            invite_wks.update_cell((row, 8), message.text)
            reply_two_languages(message, 
                "Reward address is set successfully!\nYou can type /reward_addr to check your current reward address.", 
                "接受奖励的钱包地址设置成功!\n你可以输入 /reward_addr 来查看当前设置的地址"
            )
        else:
            message.reply_text("Please register the program, get your refer link first.")
    except Exception as e:
        logger.error('set reward address ERROR: %s', e)
    finally:
        lock.release()
    
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
        row = findKey("invite_wks", str(message.from_user.id))
        logger.info(row)
        rowData = invite_wks.get_row(row)
        addr = rowData[7]
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

# def record_new_members(bot, update):
#     logger.info('new member joined %s'%update.message)
#     message = update.message
#     try:
#         if message.chat.title in MONITOR_GROUPS:
#             for member in message.new_chat_members:
#                 try:
#                     lock.acquire()
#                     logger.info(member)
#                     if(member.is_bot == True):
#                         return
#                      #check if user is old user
#                     if member.id in USER_DATA_GROUP:
#                         return 
#                     row = findKey("new_members_wks", str(member.id))
#                     if row == -1: # avoid recording users that have already existed
#                         new_member_info = [
#                             json_serial(message.date),
#                             member.username, 
#                             member.first_name,
#                             member.id,
#                             ""
#                         ]
#                         insertRow("new_members_wks", new_member_info) # record new member's infomation
#                     else: #handle user are already in our new member database #two conditions, joined by themself or joined by refer link
#                         #logger.info("user in row: %s"%row)
#                         data = new_members_wks.get_row(row)
#                         logger.info("user data row: %s"%data)
#                         code = data[4]
#                         verified = data[5]
#                         logger.info("code: %s" %code)
#                         if code != "": #user used the code then joined the group
#                             logger.info("verify user joined group after using a refer code")
#                             if verified == "Verified":
#                                 logger.info("User already verified as new member before.")
#                             else:
#                                 new_members_wks.update_cell((row, 6), "Verified") 
#                                 #add invite count for inviter
#                                 logger.info("add verified mark to user")
#                                 addInviteCount(code)
#                                 logger.info("Add invite count for inviter")
#                 except Exception as e:
#                     raise
#                 finally:
#                     lock.release()
#     except Exception as e:
#         logger.error('record new members ERROR: %s', e)

# def send_faq(bot, update):
#     try:
#         logger.info('/faq')
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         reply = "Questions list:\n"
#         faq_list = getFaqList()
#         for question in faq_list:
#             itembtn = types.KeyboardButton(question)
#             markup.add(itembtn)
#             reply = reply + "\n" + question
#         bot.sendMessage(chat_id = update.message.chat.id , text = reply , reply_markup=markup)
#     except Exception as e:
#         logger.error('/faq ERROR: %s', e)

    
########################################################## App entry #################################################################################
def main():
    """Start the bot."""
    # Create the EventHandler and pass it with bot's token.
    #updater = Updater("584897065:AAFKH1nl68ntLw8L8LeHxNmfd6gGUP0yLuY")
    updater = Updater(TOKEN, workers=32)
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler('start', start, pass_args=True))
    dp.add_handler(CommandHandler('start1', start1))
    dp.add_handler(CommandHandler('reward_addr', reward_addr))
    #dp.add_handler(CommandHandler('test', test))
    #dp.add_handler(CommandHandler('faq', send_faq))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echoMessageHandler))
    #dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, record_new_members))

    # menu handler
    
    dp.add_handler(CallbackQueryHandler(main_menu_CN, pattern='mainCN'))
    dp.add_handler(CallbackQueryHandler(join_menu_CN, pattern='joinNKNCN'))
    #dp.add_handler(CallbackQueryHandler(refer_menu_CN, pattern='referCN'))
    dp.add_handler(CallbackQueryHandler(doc_menu_CN, pattern='docCN'))
    dp.add_handler(CallbackQueryHandler(myAccount_menu_CN, pattern='myAccountCN'))

    dp.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    dp.add_handler(CallbackQueryHandler(join_menu, pattern='joinNKN'))
    #dp.add_handler(CallbackQueryHandler(refer_menu, pattern='refer'))
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