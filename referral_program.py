
#!/usr/bin/python
# -*- coding: utf-8 -*-

# NKN Bot using Google Docs 
# 2018.7.16 by Long Wang

import time
import pygsheets
import logging
import threading
import re
import sqlite3
from telebot import *
from hash import *
from config import TOKEN, SHEET_KEY, SERVICE_FILE, MONITOR_GROUPS, OUTH_FILE
import requests

from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

#import Keyboards methods
from keyBoards import *
from common import *
from menuMessages import *

#initilizing lock, logger and google sheet
LANG = 'EN'
lock = threading.Lock()
logger.setLevel(logging.INFO)
#open databse connection
conn = sqlite3.connect('nkn.db', check_same_thread=False)
c = conn.cursor()
############################### Menu event handler #########################################################################
def start(bot, update, args):
    isbot = update.message.from_user.is_bot
    if isbot == True:
        logger.info('Bot detected!!!')
        update.message.reply_text("Bot detected!!!")
        return
    userArgs = "".join(args)
    logger.info("User start event, if user is from refer link, code is : %s" %userArgs)
    if userArgs != "":
        message = update.message
        message.text = userArgs
        handle_invite_code(message)
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
        query = update.callback_query
        from_user = query.from_user
        logger.info('/myAccount from user: %s, %s'%(from_user.id, from_user.username))
        user_data = c.execute("SELECT * FROM USER WHERE ID=?", (from_user.id, )).fetchone()
        if user_data:
            logger.info("Fetch user data from USER table: ")
            logger.info(user_data)
            reply = u"Hello %s\nYou invited %s friends\nYou have %s points" %(from_user.username, user_data[5], user_data[8])
        else:
            logger.info("User not enrolled in program yet.")
            reply = "You haven't join the program yet, please get your referral link first, bot will enroll you in to the program once you generate your referal link."
        bot.edit_message_text(chat_id=query.message.chat_id,
                    message_id=query.message.message_id,
                    text=reply,
                    reply_markup=back_menu_keyboard())
    except Exception as e:
        logger.error('/myAccount ERROR: %s', e)

@run_async
def myAccount_menu_CN(bot, update):
    try:
        query = update.callback_query
        from_user = query.from_user
        logger.info('/myAccount from user: %s, %s'%(from_user.id, from_user.username))
        user_data = c.execute("SELECT * FROM USER WHERE ID=?", (from_user.id, )).fetchone()
        print(user_data)
        if user_data:
            logger.info("Fetch user data from USER table: ")
            logger.info(user_data)
            reply = u"您好 %s\n您目前已经邀请了 %s 位朋友\n你现在一共有 %s 分" %(from_user.username, user_data[5], user_data[8])
        else:
            logger.info("User not enrolled in program yet.")
            reply = "您还没有加入这个项目，请先获得你的邀请链接, 机器人会自动帮您注册。"
        bot.edit_message_text(chat_id=query.message.chat_id,
                    message_id=query.message.message_id,
                    text=reply,
                    reply_markup=back_menu_keyboard_CN())
    except Exception as e:
        logger.error('/myAccount ERROR: %s', e)
       
@run_async
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

@run_async
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

@run_async
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

@run_async
def refer_menu(bot, update):
    try:
        lock.acquire()
        from_user = update.callback_query.message.chat
        code = generateInviteCode("NKN", from_user.id)
        logger.info("referal link requested.")
        user_data = c.execute("SELECT * FROM USER WHERE ID=?", (from_user.id, )).fetchone()
        if user_data:
            logger.info("User found in database. return link: %s"%code)
        else:
            user = (from_user.id, from_user.username, from_user.first_name, from_user.last_name, code, 0,0,0,0,'')
            logger.info("User not found, insert user in database")
            logger.info(user)
            c.execute('INSERT INTO USER VALUES (?,?,?,?,?,?,?,?,?,?)', user)
            conn.commit()
    except Exception as e:
        logger.error('/invite ERROR: %s', e)
    finally:
        lock.release()
    query = update.callback_query
    bot.edit_message_text(chat_id=query.message.chat_id,
                                message_id=query.message.message_id,
                                text=refer_menu_message(code),
                                reply_markup=back_menu_keyboard())
    
@run_async
def refer_menu_CN(bot, update):
    try:
        lock.acquire()
        from_user = update.callback_query.message.chat
        code = generateInviteCode("NKN", from_user.id)
        logger.info("/referal link requested.")
        user_data = c.execute("SELECT * FROM USER WHERE ID=?", (from_user.id, )).fetchone()
        if user_data:
            logger.info("User found in database. return link: %s"%code)
        else:
            user = (from_user.id, from_user.username, from_user.first_name, from_user.last_name, code, 0,0,0,0,'')
            logger.info("User not found, insert user in database")
            logger.info(user)
            c.execute('INSERT INTO USER VALUES (?,?,?,?,?,?,?,?,?,?)', user)
            conn.commit()
    except Exception as e:
        logger.error('/invite ERROR: %s', e)
    finally:
        lock.release()
    query = update.callback_query
    bot.edit_message_text(chat_id=query.message.chat_id,
                                message_id=query.message.message_id,
                                text=refer_menu_message(code),
                                reply_markup=back_menu_keyboard_CN())

# def getFaqList():
#     # find faq questions
#     faq_filter = re.compile(r'^Q\d+\..')
#     cell_list = reply_wks.find(faq_filter)
#     faq_list = []
#     for question in cell_list:
#         faq_list.append(question.value)
#     return faq_list



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

@run_async
def handle_invite_code(message):
    try:
        logger.info('/handle invite code from user: %s'%message.from_user.username)
        userID = message.from_user.id
        from_user = message.from_user
        #check if the invite code exist
        invite_code = c.execute("SELECT * FROM USER WHERE INVITE_CODE=?", (message.text, )).fetchone()
        if not invite_code:
            logger.info("The invite code doesn't exist.")
            reply_two_languages(message, "Invalid invitation code, the invitation code doesn't exist.", "邀请码不存在")
            return 
        
        #check if user's code is matching his own code
        code = generateInviteCode("NKN", userID)
        if code == message.text:
            logger.info("You can't use your own invite code.")
            reply_two_languages(message, "You can't use your own invite code.", "你不能使用自己的邀请码")
            return

        #check if user is an old user
        user_data = c.execute("SELECT * FROM USER WHERE ID=?", (userID, )).fetchone()
        new_member_data = c.execute("SELECT * FROM NEW_MEMBERS WHERE ID=?", (userID, )).fetchone()
        old_groupCN_user_data = c.execute("SELECT * FROM NKN_GROUP_USER_CN WHERE ID=?", (userID, )).fetchone()
        old_groupEN_user_data = c.execute("SELECT * FROM NKN_GROUP_USER_EN WHERE ID=?", (userID, )).fetchone()
        if all(v is None for v in [user_data, new_member_data, old_groupEN_user_data, old_groupCN_user_data]):
            logger.info("User verified as new user, not in our database.")
        else:
            logger.info("User are not a new member.")
            reply_two_languages(message, "Use invitation code failed, our records shows you are in our group or you were in the group before.", "邀请码使用无效，我们记录显示你不是我们新群用户") 
            return

        #if user is not an old group user
        #and code is exsits and not user's own code
        #we insert user to new_member table and user table
        try:
            lock.acquire()
            new_member_user_data = (from_user.id, from_user.username, from_user.first_name, from_user.last_name, json_serial(message.date), message.text,'')
            user_data = (from_user.id, from_user.username, from_user.first_name, from_user.last_name, code, 0,0,0,0,'')
            logger.info(new_member_user_data)
            c.execute('INSERT INTO NEW_MEMBERS VALUES (?,?,?,?,?,?,?)', new_member_user_data)
            logger.info(user_data)
            c.execute('INSERT INTO USER VALUES (?,?,?,?,?,?,?,?,?,?)', user_data)
            logger.info("Inserted sucessfully")
            conn.commit()
            reply_two_languages(message, 
                "The code is used successfully! we will verify it after you join NKN group.\nIf you haven't set your reward address, you can reply your wallet address to the bot. Candies will be send to the address after the activity.", 
                "邀请码使用成功! 当你加入NKN群之后，我们会进行验证。\n积分可以兑换糖果哦，如果您还没有绑定NEO钱包，可以给机器人回复您的钱包地址进行设置，活动结束后奖励会发送到对应的地址"
            )
        except Exception as e:
            raise
        finally:
            lock.release()
    except Exception as e:
        logger.error('use invite code ERROR: %s', e)

# # handle reward address	
@run_async
def handle_reward_addr(message):
    try:
        lock.acquire()
        from_user = message.from_user
        userID = from_user.id
        logger.info("handle_reward_addr from user: %s"%from_user.username)
        user_data = c.execute("SELECT * FROM USER WHERE ID=?", (userID, )).fetchone()
        if user_data:
            t = (message.text, userID)
            c.execute('UPDATE USER SET NEO_ADDRESS = ? WHERE ID = ?', t)
            conn.commit()
            logger.info("Update NEO wallet address sucessfully")
            reply_two_languages(message, 
                "Reward address is set successfully!\nYou can type /reward_addr to check your current reward address.", 
                "接受奖励的钱包地址设置成功!\n你可以输入 /reward_addr 来查看当前设置的地址"
            )
        else:
            message.reply_text("You havn't register the program yet, please generate your referral link fisrt by clicking Refer friends button.")
    except Exception as e:
        logger.error('set reward address ERROR: %s', e)
    finally:
        lock.release()
    
def reward_addr(bot, update):
    check_reward_addr(update.message)

def check_reward_addr(message):
    try:
        from_user = message.from_user
        userID = from_user.id
        neo_address = c.execute("SELECT NEO_ADDRESS FROM USER WHERE ID=?", (userID, )).fetchone()
        print(neo_address)
        if not neo_address:
            logger.info("User not found")
            en_reply = "We don't find your record in our database, please register the program first by clicking the Refer friends button"
            cn_reply = "没有找到您的信息，请先点击邀请朋友按钮来注册积分系统。"
            reply_two_languages(message, en_reply, cn_reply)  
            return
        
        if neo_address[0] != '':
            logger.info("NEO address found: %s"%neo_address)
            en_reply = "Your current reward address is %s\nIf you want to change the address, you can reply a new address to the bot." % neo_address
            cn_reply = u"当前设置的接受奖励的钱包地址为: %s\n如果你想更换钱包地址，可以给机器人回复一个新的地址" % neo_address 
            reply_two_languages(message, en_reply, cn_reply)
        else:
            logger.info("NEO address not found")
            en_reply = "You haven't set your reward address yet. You can reply your wallet address to the bot to set it."
            cn_reply = "你还未设置用于接受奖励的钱包地址，你可以通过给机器人发送钱包地址来进行设置"
            reply_two_languages(message, en_reply, cn_reply)    
    except Exception as e:
        logger.error('get reward address ERROR: %s', e)

@run_async
def record_new_members(bot, update):
    logger.info('/new member joined')
    message = update.message
    from_user = message.from_user
    try:
        if message.chat.title in MONITOR_GROUPS:
            for member in message.new_chat_members:
                try:
                    lock.acquire()
                    logger.info(member)
                    #record_member(member)
                    if(member.is_bot == True):
                        return
                    #check if user is an old user
                    userID = member.id
                    user_data = c.execute("SELECT * FROM USER WHERE ID=?", (userID, )).fetchone()
                    new_member_data = c.execute("SELECT * FROM NEW_MEMBERS WHERE ID=?", (userID, )).fetchone()
                    
                    if all(v is None for v in [user_data, new_member_data]):
                        logger.info("User joined without referral. Insert new member")
                        new_member_user_data = (from_user.id, from_user.username, from_user.first_name, from_user.last_name, json_serial(message.date), '','')
                        c.execute('INSERT INTO NEW_MEMBERS VALUES (?,?,?,?,?,?,?)', new_member_user_data)
                        conn.commit()
                        logger.info("Inser user successfully")
                        logger.info(new_member_user_data)
                        return

                    logger.info("new_member_data")
                    logger.info(new_member_data)
                    if new_member_data:
                        if new_member_data[6] == "Verified":
                            logger.info("User already verified before")
                            return
                        logger.info("Verified user, update NEW_MEMBERS table with VERIFIED")
                        t = (userID,)
                        c.execute("UPDATE NEW_MEMBERS SET VERIFIED = 'Verified' WHERE ID = ?", t)
                        
                        logger.info("Update new member reward 100 points for user")
                        t = (userID,)
                        c.execute("UPDATE USER SET NEW_MEMBER_REWARD_POINTS = 100, TOTAL_POINTS = 100 WHERE ID = ?", t)
                        
                        refer_by = new_member_data[5]
                        inviter_data = c.execute("SELECT * FROM USER WHERE INVITE_CODE=?", (refer_by, )).fetchone()
                        print(inviter_data)
                        inviter_id = inviter_data[0]
                        inviter_count = inviter_data[5]+1
                        if inviter_count > 100:
                            inviter_count = 100
                        invite_points = inviter_count * 100
                        invite_total_points = invite_points + inviter_data[7]
                        t = (inviter_count, invite_points, invite_total_points, inviter_id)
                        c.execute("UPDATE USER SET INVITE_COUNT=?, INVITE_POINTS=?, TOTAL_POINTS=? WHERE ID = ?", t)
                        conn.commit()
                        logger.info("Update inviter count %s and total_points: %s"%(inviter_count, invite_total_points))
                        logger.info("Update data successfully")
                    else:
                        logger.info("\n")
                        return
                except Exception as e:
                    raise
                finally:
                    lock.release()
    except Exception as e:
        logger.error('record new members ERROR: %s', e)


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