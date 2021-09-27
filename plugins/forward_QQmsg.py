import config
import nonebot
from nonebot import on_natural_language, NLPSession
import wxpush
from nonebot.log import logger


@on_natural_language(only_to_me=False, only_short_message=False, allow_empty_message=True)
async def _(session: NLPSession, ):
    bot = nonebot.get_bot()
    login = await bot.get_login_info()
    print(login)
    # 转发群消息
    if session.ctx['message_type'] == 'group':
        group_id = session.ctx['group_id']
        user_id = session.ctx['user_id']
        if group_rule(session):
            # 获取群名字和群友昵称
            group_name = (await bot.get_group_info(group_id=group_id))['group_name']
            user_name = session.ctx['sender']['card']
            if user_name == '':
                user_name = session.ctx['sender']['nickname']
            # 拼接消息
            raw_message = raw_msg(session)
            send_msg = str('群聊：' + group_name + '\n发送人：' + user_name + '\n--------------\n' + raw_message)
            wxpush.main(send_msg)

    # 转发私聊消息
    elif session.ctx['message_type'] == 'private':
        user_id = session.ctx['user_id']
        if pravatechat_rule(session):
            # 获取发送人备注
            friend_list = (await bot.get_friend_list())
            friend_name = session.ctx['sender']['nickname']
            for item in friend_list:
                if item['user_id'] == user_id:
                    friend_name = item['remark']
                    break
            # 拼接消息
            raw_message = raw_msg(session)
            send_msg = str('发送人：' + friend_name + '\n--------------\n' + raw_message)
            wxpush.main(send_msg)


# 判断私聊信息是否在规则内
def pravatechat_rule(session):
    user_id = session.ctx['user_id']
    if config.pravitechat_rule['rule_type'] == 1 and user_id not in config.pravitechat_rule['blacklist']:
        logger.info('私聊消息黑名单规则：好友' + str(user_id) + '不在黑名单中，转发该条消息')
        return True
    elif config.pravitechat_rule['rule_type'] == 2 and user_id in config.pravitechat_rule['whitelist']:
        logger.info('私聊消息白名单规则：好友' + str(user_id) + '在白名单中，转发该条消息')
        return True
    elif config.pravitechat_rule['rule_type'] == 3:
        logger.info('私聊消息全部转发：好友' + str(user_id) + '在名单中，转发该条消息')
        return True
    else:
        return False


# 判断群信息是否在规则内
def group_rule(session):
    group_id = session.ctx['group_id']
    user_id = session.ctx['user_id']
    if config.group_rule['rule_type'] == 1 and group_id not in config.group_rule['blacklist']:
        logger.info('群聊消息黑名单规则：群聊' + str(group_id) + '群友' + str(user_id) + '不在黑名单中，转发该条消息')
        return True
    elif config.group_rule['rule_type'] == 2 and \
            str(group_id) in config.group_rule['whitelist'].keys() and \
            (user_id in config.group_rule['whitelist'][str(group_id)] or len(
                config.group_rule['whitelist'][str(group_id)]) == 0):
        logger.info('群聊消息白名单规则：群聊' + str(group_id) + '群友' + str(user_id) + '在白名单中，转发该条消息')
        return True
    elif config.group_rule['rule_type'] == 3:
        logger.info('群聊消息全部转发：群聊' + str(group_id) + '群友' + str(user_id) + '在名单中，转发该条消息')
        return True
    else:
        return False


# 解析拼接原始消息
def raw_msg(session):
    raw_message = ''
    for i in range(len(session.ctx['message'])):
        message_type = session.ctx['message'][i]['type']
        if message_type == 'text':
            raw_message += session.ctx['message'][i]['data']['text']
        elif message_type == 'image':
            raw_message += '<a href="' + session.ctx['message'][i]['data']['url'] + '">图片消息</a>'
        elif message_type == 'at':
            raw_message += '【At消息】'
        elif message_type == 'face':
            raw_message += '【表情消息】'
        elif message_type == 'reply':
            raw_message += '【回复消息】'
        elif message_type == 'video':
            raw_message += '【视频消息】'
        elif message_type == 'record':
            raw_message += '【语音消息】'
        else:
            raw_message = '【不支持的消息类型】'
    return raw_message
