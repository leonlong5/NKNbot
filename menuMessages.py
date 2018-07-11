############################# Messages #########################################
def main_menu_message():
    return """ Hello, I'm NKN Bot. Welcome to the NKN group. I'm here to help you know more about NKN.
        Here are some official links:
        NKN Official Site: https://www.nkn.org
        NKN Official Twitter: https://twitter.com/NKN_ORG/
        NKN Official Email: contact@nkn.org"""
    
def main_menu_message_CN():
    return """你好，我是NKN机器人，欢迎来到NKN。我会帮助你更好的了解更多有关于NKN的信息。
        这里有一些官方链接:
        NKN 官方网页: https://www.nkn.org
        NKN 官方 Twitter: https://twitter.com/NKN_ORG/
        NKN 官方 Email: contact@nkn.org"""
    
def joinNKN_menu_message():
    return 'English: https://t.me/nknorg \n中文群: https://t.me/nknorgCN'

def second_menu_message():
    return 'Choose the submenu in second menu:'

def refer_menu_message(code, count):
    #link = "https://t.me/NKNrobot?start="+code
    return "Your invite code is:  %s \nYou have already invited %s people" % (code, count)

def refer_menu_message_CN(code, count):
    #link = "https://t.me/NKNrobot?start="+code
    return u"你的邀请码是:  %s\n你已经邀请了 %s 个人" % (code, count)