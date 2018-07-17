#!/usr/bin/python
# -*- coding: utf-8 -*-

# Data organization for NKN bot
# 2018.7.15, Long Wang

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
lock = threading.Lock()
logger.setLevel(logging.INFO)
gc = pygsheets.authorize(outh_file=OUTH_FILE)
sh = gc.open('NKNbot') # Open spreadsheet and then workseet

# <Worksheet '新加群名单' index:1>
# <Worksheet '接受奖励地址' index:2>
# <Worksheet '邀请数量统计' index:3>
reply_wks = sh.sheet1 # reply sheet
new_members_wks = sh.worksheet(value=1) # record new group members
invite_wks = sh.worksheet(value=3) # count invite number 

NEW_MEMBERS_DATA = new_members_wks.get_all_values()
IVITE_DATA = invite_wks.get_all_values()


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
    cell_list = wks.find(key)
    if len(cell_list) == 0:
        return -1
    else:
        return cell_list[0].row

def insertRow(wks, values, end_flag='--END--'):
    row = findKey(wks, end_flag)
    logger.info("insert row: %s"%row)
    if row != -1:
        wks.insert_rows(row-1, values=values)
        
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

def getPoints(invite_row_data, new_member_data, invite_row_key):
    points = 0
    #check if user used a refer code 
    if new_member_data:
        ref = new_member_data[5]
        logger.info("User verified join group?%s" %ref)
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
            invite_wks.update_cell((invite_row_key, 7), points)
    return points

    
########################################################## App entry #################################################################################
def main():
    #add new member points to invite sheet
    count = 0
    for item in NEW_MEMBERS_DATA:
        username = item[1]
        first_name = item[2]
        last_name = ""
        userID = item[3]
        referCode = item[4]
        verified = item[5] 
        code = generateInviteCode("NKN", userID)
        row = findKey(invite_wks, str(userID))
        logger.info("Find the row by userID: %s"%userID)
        # if row != -1:
        #     if verified == "Verified":
        #         invite_wks.update_cell((row, 10), 100)
        #         logger.info("Update the invite sheet with verified member. 100")
        #     else:
        #         invite_wks.update_cell((row, 10), 0)
        #         logger.info("Update the invite sheet with verified member. 0")
        if row == -1:
            logger.info("User not in invite sheet. Verified? %s"%verified)
            if verified == "Verified":
                count = count + 1
                logger.info("Insert into invite sheet, number: %s"%count)
                values = [
                    username,
                    first_name,
                    last_name,
                    userID,
                    code, 
                    0,
                    '',
                    '',
                    0,
                    100
                ]
                insertRow(invite_wks, values) 


if __name__ == '__main__':
    main()