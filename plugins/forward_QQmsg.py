import config
import nonebot
from nonebot import on_natural_language, NLPSession
import wxpush


@on_natural_language(only_to_me=False)
async def _(session: NLPSession, ):
    bot = nonebot.get_bot()
    # 转发群消息
    if session.ctx['message_type'] == 'group':
        # 获取群号码
        group_id = session.ctx['group_id']
        # logger.info(str(group_id) in config.group_rule['whitelist'].keys())
        # 获取发送人号码
        user_id = session.ctx['user_id']
        if (config.group_rule['rule_type'] == 1 and group_id not in config.group_rule['blacklist']) or \
                (config.group_rule['rule_type'] == 2 and str(group_id) in config.group_rule['whitelist'].keys() and
                 (user_id in config.group_rule['whitelist'][str(group_id)] or
                  len(config.group_rule['whitelist'][str(group_id)]) == 0)) or \
                config.group_rule['rule_type'] == 3:
            # 获取群昵称
            group_name = (await bot.get_group_info(group_id=session.ctx['group_id']))['group_name']
            # 获取发送人群名字
            user_name = session.ctx['sender']['card']
            if user_name == '':
                user_name = session.ctx['sender']['nickname']
            # 原始消息
            raw_message = raw_msg(session)
            send_msg = str('群聊：' + group_name + '\n发送人：' + user_name + '\n\n' + raw_message)
            wxpush.main(send_msg)

    # 转发私聊消息
    elif session.ctx['message_type'] == 'private':
        # 获取发送人号码
        user_id = session.ctx['user_id']
        if (config.pravitechat_rule['rule_type'] == 1 and user_id not in config.pravitechat_rule['blacklist']) or \
                (config.pravitechat_rule['rule_type'] == 2 and user_id in config.pravitechat_rule['whitelist']) or \
                config.pravitechat_rule['rule_type'] == 3:
            # 获取发送人备注
            friend_list = (await bot.get_friend_list())
            friend_name = ''
            for item in friend_list:
                if item['user_id'] == user_id:
                    friend_name = item['remark']
                    break
            # 原始消息
            raw_message = raw_msg(session)
            send_msg = str('发送人：' + friend_name + '\n\n' + raw_message)
            wxpush.main(send_msg)


# 解析拼接原始消息
def raw_msg(session):
    raw_message = ''
    for i in range(len(session.ctx['message'])):
        message_type = session.ctx['message'][i]['type']
        if message_type == 'text':
            raw_message += session.ctx['message'][i]['data']['text'] + '\n'
        elif message_type == 'image':
            raw_message += '<a href="' + session.ctx['message'][i]['data']['url'] + '">图片消息</a>\n'
        elif message_type == 'video':
            raw_message += '【视频消息】\n'
        elif message_type == 'record':
            raw_message += '【语音消息】\n'
        elif message_type == 'face':
            raw_message += '【表情消息】\n'
        else:
            raw_message = '【不支持的消息类型】\n'
    return raw_message
