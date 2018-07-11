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

def refer_menu_message(code, count):
    link = "https://t.me/NKNrobot?start="+code
    return "Your invite link is:\n  %s \nYou have already invited %s people" % (link, count)

def refer_menu_message_CN(code, count):
    link = "https://t.me/NKNrobot?start="+code
    return u"你的邀请连接是:\n  %s\n你已经邀请了 %s 个人" % (link, count)

def NKN_doc_CN():
    return """📖基本文档
NKN 英文白皮书: t.me/nknorg/43545 
NKN 经济模型: t.me/nknorg/35053
NKN产品路线图：https://t.me/nknorgCN/19949
AMA Apr 2018: t.me/nknorg/43548 

🎭社交媒体
Telegram Channels:
    News: https://t.me/nknetwork
    English Channel:https://t.me/nknorg
    Chinese Channel: https://t.me/nknorgCN
Twitter: https://twitter.com/NKN_ORG/
Github:https://github.com/nknorg
Medium: https://medium.com/nknetwork
Facebook: https://www.facebook.com/nkn.org
Reddit:https://www.reddit.com/r/nknblockchain/
微信公众号：NKN_News

🎬NKN视频
AMA: https://www.youtube.com/watch?v=u7K0NeTeB3M&t=129s
NEO Global Capital介绍NKN项目: https://youtu.be/_yQGHFIaqhg?t=15m35s
Boxmining对NKN创始人访谈: https://www.youtube.com/watch?v=o95Uu4m_hXw&feature=youtu.be
Boxmining介绍NKN项目: https://www.youtube.com/watch?v=aFR9k8IPEdw&feature=youtu.be
AMTV介绍NKN项目:https://youtu.be/vYRCW7hTN4E"""