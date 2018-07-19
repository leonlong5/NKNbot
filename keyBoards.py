from telegram import InlineKeyboardButton, InlineKeyboardMarkup

############################ Keyboards #########################################
def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Join NKN group', callback_data='joinNKN')],
                [InlineKeyboardButton('Refer friends', callback_data='refer')],
                [InlineKeyboardButton('Documents', callback_data='doc')],
                [InlineKeyboardButton('My Account', callback_data='myAccount'), InlineKeyboardButton('Language', callback_data='Lang')]]
    return InlineKeyboardMarkup(keyboard)

def main_menu_keyboard_CN():
    keyboard = [[InlineKeyboardButton('加入NKN', callback_data='joinNKNCN')],
                [InlineKeyboardButton('邀请朋友', callback_data='referCN')],
              [InlineKeyboardButton('文档', callback_data='docCN')],
              [InlineKeyboardButton('我的账户', callback_data='myAccountCN'), InlineKeyboardButton('语言', callback_data='Lang')]]
    return InlineKeyboardMarkup(keyboard)

def language_menu_keyboard():
    keyboard = [[InlineKeyboardButton('English', callback_data='EN'), InlineKeyboardButton('中文', callback_data='CN')]]
    return InlineKeyboardMarkup(keyboard)

def back_menu_keyboard_CN():
    keyboard = [[InlineKeyboardButton('返回', callback_data='mainCN')]]
    return InlineKeyboardMarkup(keyboard)

def back_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Back', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)

