#!/usr/bin/python
# -*- coding: utf-8 -*-

# NKN Bot using Google Docs 
# 2018.6.6 by Shunda

import time
import pygsheets
import logging
import threading
from telebot import *
from hash import *
from config import TOKEN, SHEET_KEY, SERVICE_FILE, MONITOR_GROUPS, OUTH_FILE
import requests

lock = threading.Lock()

logger.setLevel(logging.INFO)
bot = TeleBot(TOKEN)

#gc = pygsheets.authorize(service_file=SERVICE_FILE)
#sh = gc.open_by_key(SHEET_KEY)

gc = pygsheets.authorize(outh_file=OUTH_FILE)
sh = gc.open('NKNbot') # Open spreadsheet and then workseet

# <Worksheet '新加群名单' index:1>
# <Worksheet '接受奖励地址' index:2>
# <Worksheet '邀请数量统计' index:3>
reply_wks = sh.sheet1 # reply sheet
new_members_wks = sh.worksheet(value=1) # record new group members
addr_wks= sh.worksheet(value=2) # record reward addresses
invite_wks = sh.worksheet(value=3) # count invite number 


@bot.message_handler(commands=['start'])
def handler_start(message):
    try:
        logger.info('/start')
        reply = getValue('/start')
        print(message)
        if reply != "":
            bot.send_message(message.chat.id, reply)
    except Exception as e:
        logger.error('/start ERROR: %s', e)

@bot.message_handler(commands=['help'])
def handler_start(message):
    try:
        logger.info('/help')
        reply = getValue('/help')
        if reply != "":
            bot.send_message(message.chat.id, reply)
    except Exception as e:
        logger.error('/help ERROR: %s', e)

@bot.message_handler(commands=['doc'])
def handler_start(message):
    try:
        logger.info('/doc')
        reply = getValue('/doc')
        if reply != "":
            bot.send_message(message.chat.id, reply)
    except Exception as e:
        logger.error('/doc ERROR: %s', e)

@bot.message_handler(commands=['MyAccount'])
def handler_start(message):
    try:
        logger.info('/MyAccount')
        reply = getAccount(str(message.from_user.id))
        if reply != "":
            bot.send_message(message.chat.id, "Username: "+reply)
    except Exception as e:
        logger.error('/doc ERROR: %s', e)

@bot.message_handler(commands=['faq'])
def send_faq(message):
    try:
        logger.info('/faq')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        reply = "Questions list:\n"
        faq_list = getFaqList()
        for question in faq_list:
            itembtn = types.KeyboardButton(question)
            markup.add(itembtn)
            reply = reply + "\n" + question
        bot.send_message(message.chat.id, reply, reply_markup=markup)
    except Exception as e:
        logger.error('/faq ERROR: %s', e)

@bot.message_handler(commands=['invite'])
def get_invite_code(message):
    try:
        lock.acquire()
        logger.info('/invite')
        from_user = message.from_user
        print(from_user)
        code = generateInviteCode("NKN", from_user.id)
        count = getInviteCount(str(from_user.id))
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
        en_reply = "Your invite code is:  %s\nYou have already invited %s people" % (code, count)
        cn_reply = u"你的邀请码是:  %s\n你已经邀请了 %s 个人" % (code, count)
        reply_two_languages(message, en_reply, cn_reply)
    except Exception as e:
        logger.error('/invite ERROR: %s', e)
    finally:
        lock.release()

@bot.message_handler(content_types=['new_chat_members'])
def record_new_members(message):
    try:
        if message.chat.title in MONITOR_GROUPS:
            logger.info('new member')
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
                            timestamp_datetime(message.date), 
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

# handle invite code
@bot.message_handler(regexp="^NKN[A-F0-9]{5}")
def handle_invite_code(message):
    try:
        logger.info('invite code')
        #check if the code exist
        if checkCodeExistence(message.text):
            reply_two_languages(message, "The invite code doesn't exist.", "邀请码不存在")
            return 
        print(checkCodeExistence(message.text))
        #check if user's code is matching his own code
        code = generateInviteCode("NKN", message.from_user.id)
        print(code)
        if code == message.text:
            reply_two_languages(message, "You can't use your own invite code.", "你不能使用自己的邀请码")
            return
        try:
            lock.acquire()
            #check if user already exists in our db
            exist = findUser(new_members_wks, str(message.from_user.id))
            
            if exist != -1:
                #new user, need to create new account, insert to new_members_wks
                    new_member_info = [
                            timestamp_datetime(message.date), 
                            message.from_user.username, 
                            message.from_user.first_name,
                            message.from_user.id,
                            message.text
                    ]
                    insertRow(new_members_wks, new_member_info) 
                    #add invite count for inviter
                    if addInviteCount(message.text) == -1:
                        logger.info('Invalid invite code');
                    else:
                        logger.info('Invite count added');
                    # row = findKey(invite_wks, message.text)
                    # invite_wks.update_cell((row, 5), message.text)
                    logger.info(str(message.from_user.id) + ":" + message.text)
                    reply_two_languages(message, 
                        "The code is used successfully!\nIf you haven't set your reward address, you can reply your wallet address to the bot. Candies will be sent to the address after the activity.", 
                        "邀请码使用成功!\n如果你未设置过接受奖励的钱包地址，可以给机器人回复你的钱包地址进行设置，活动结束后奖励会发送到对应的地址"
                    )
            else:
               reply_two_languages(message, "You aren't a new member of NKN group.", "你不是一个新加群的用户, 无法使用邀请码")
        except Exception as e:
            raise
        finally:
            lock.release()
    except Exception as e:
        logger.error('use invite code ERROR: %s', e)

# /reward_addr : check current reward address
@bot.message_handler(commands=['reward_addr'])
def check_reward_addr(message):
    try:
        row = findKey(addr_wks, str(message.from_user.id))
        if row != -1:
            addr = addr_wks[row-1][4]
            print(addr_wks)
            en_reply = "Your current reward address is %s\nIf you want to change the address, you can reply a new address to the bot." % addr
            cn_reply = u"当前设置的接受奖励的钱包地址为: %s\n如果你想更换钱包地址，可以给机器人回复一个新的地址" % addr 
            reply_two_languages(message, en_reply, cn_reply)
        else:
            en_reply = "You haven't set your reward address yet. You can reply your wallet address to the bot to set it."
            cn_reply = "你还未设置用于接受奖励的钱包地址，你可以通过给机器人发送钱包地址来进行设置"
            reply_two_languages(message, en_reply, cn_reply)
    except Exception as e:
        logger.error('get reward address ERROR: %s', e)

# handle reward address
@bot.message_handler(regexp="[a-z0-9]{34}")
def handle_reward_addr(message):
    try:
        lock.acquire()
        from_user = message.from_user
        row = findKey(addr_wks, str(from_user.id))
        if row != -1:
            addr_wks.update_cell((row, 5), message.text)
        else:
            addr_info = [
                from_user.username,
                from_user.first_name,
                from_user.last_name,
                from_user.id,
                message.text
            ]
            insertRow(addr_wks, addr_info)
        reply_two_languages(message, 
            "Reward address is set successfully!\nYou can type /reward_addr to check your current reward address.", 
            "接受奖励的钱包地址设置成功!\n你可以输入 /reward_addr 来查看当前设置的地址"
        )
    except Exception as e:
        logger.error('set reward address ERROR: %s', e)
    finally:
        lock.release()


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
    row = findKey(invite_wks, key)
    print(row)
    if row != -1:
        # return reply_wks[row-1][0]
        return invite_wks.get_value((row, 1)) # 第一列作为回复
    else:
        return ""

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

def reply_two_languages(message, en_reply, cn_reply):
    if message.from_user.language_code == "zh-CN":
        bot.reply_to(message, cn_reply)
    else:
        bot.reply_to(message, en_reply)

def timestamp_datetime(value):
    format = '%Y-%m-%d %H:%M:%S'
    # value为传入的值为时间戳(整形)，如：1332888820
    value = time.localtime(value)
    ## 经过localtime转换后变成
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    dt = time.strftime(format, value)
    return dt

if __name__ == '__main__':
    bot.infinity_polling(True)