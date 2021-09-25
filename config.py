from nonebot.default_config import *

HOST = '127.0.0.1'
PORT = 8881
DEBUG = False


# 推送渠道配置
# pushplus_token和qywx_config为各自配置，不用多说
# 默认走所有推送渠道，不走某渠道留空。
push_way = {
    'pushplus_token': '',
    'qywx_config': {
        'wx_aid': '10000',
        'wx_cid': 'ww1000009172459ba6',
        'wx_secret': 'Wibu84141414SV-ZsF4d9T_6n4GHDoko2EOwf6zc',
    }
}


# 群消息规则配置
# 群消息可设置群黑/白名单，群内成员白名单。
# rule_type为int，只能填1,2,3。1开启黑名单，blacklist生效；2开启白名单，whitelist生效；3不开启黑白名单，全部转发。
# blacklist为int[]，填写群号码，注意：QQ群设置屏蔽群消息的群本生就在黑名单里，不用在此添加。
# whitelist为dict，其中key为string，填白名单群号码；value为int[]，填群里白名单成员号码，为空则无群成员白名单。
# 比如以下配置为：转发群1234567中成员245436666和成员222555的消息，转发群111111的全部消息
group_rule = {
    'rule_type': 2,
    'blacklist': [88888888, 99999999],
    'whitelist': {
        '1234567': [245436666, 222555],
        '111111': []
    }
}

# 私聊消息规则配置
# 私聊消息可设置黑/白名单
# rule_type为int，只能填1,2,3。1开启黑名单，blacklist生效；2开启白名单，whitelist生效；3不开启黑白名单，全部转发。
# blacklist为int[]，填写好友号码。
# whitelist为int[]，填写好友号码。
# 比如以下配置为：不转发好友88888888和99999999的消息
pravitechat_rule = {
    'rule_type': 1,
    'blacklist': [88888888, 99999999],
    'whitelist': [4144896312, 99999999],
}



