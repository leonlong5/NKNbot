############################# Messages #########################################
def main_menu_message():
    # return """ Hello, I'm NKN Bot. Welcome to the NKN group. I'm here to help you know more about NKN.
    #     Here are some official links:
    #     NKN Official Site: https://www.nkn.org
    #     NKN Official Twitter: https://twitter.com/NKN_ORG/
    #     NKN Official Email: contact@nkn.org"""
    return """The event has ended successfully，new invited user will not be recorded, thank you for your support. Please follow NKN to find more activities in the near furture."""

def main_menu_message_CN():
    # return """你好，我是NKN机器人，欢迎来到NKN。我会帮助你更好的了解更多有关于NKN的信息。
    #     这里有一些官方链接:
    #     NKN 官方网页: https://www.nkn.org
    #     NKN 官方 Twitter: https://twitter.com/NKN_ORG/
    #     NKN 官方 Email: contact@nkn.org"""
    return """活动已经成功结束，新邀请的用户将不会被记录，谢谢您的支持。请关注NKN未来的其他活动。"""
    
def joinNKN_menu_message():
    return 'English: https://t.me/nknorg \n中文群: https://t.me/nknorgCN'

def refer_menu_message(code):
    link = "https://t.me/NKNrobot?start="+code
    return "Your invite link is:\n%s" %link

def refer_menu_message_CN(code):
    link = "https://t.me/NKNrobot?start="+code
    return u"你的邀请连接是:\n%s" %link

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

def NKN_doc():
    return """"NKN Essential Docs:
📖NKN Whitepaper: t.me/nknorg/43545
📖NKN Economic Model, Token Metrics & Roadmap: t.me/nknorg/35053
📖Supplemental Token Metrics Info: t.me/nknorg/35056
📖Written AMA Apr 2018: t.me/nknorg/43548

Videos:
AMA: https://www.youtube.com/watch?v=u7K0NeTeB3M&t=129s
NEO Global Capital had shared about NKN: https://youtu.be/_yQGHFIaqhg?t=15m35s
NKN interview by Boxmining: https://www.youtube.com/watch?v=o95Uu4m_hXw&feature=youtu.be
Short video on NKN introduction by Boxmining: https://www.youtube.com/watch?v=aFR9k8IPEdw&feature=youtu.be
Live interview with Ivan on tech: https://t.co/Ch6kN0M3e4
Testnet preview demo: https://www.youtube.com/watch?v=0Kluy9YjTVI&feature=youtu.be"""