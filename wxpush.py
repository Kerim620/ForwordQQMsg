import json
import xmltodict
import config
import requests
from nonebot.log import logger


def qywx(msg, config):
    get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={config['wx_cid']}&corpsecret={config['wx_secret']}"
    response = requests.get(get_token_url).content
    if json.loads(response).get('errmsg') != 'ok':
        return False
    access_token = json.loads(response).get('access_token')
    if access_token and len(access_token) > 0:
        send_msg_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
        data = {
            "touser": '@all',
            "agentid": config['wx_aid'],
            "msgtype": "text",
            "text": {
                "content": msg
            },
            "duplicate_check_interval": 600
        }
        r = requests.post(send_msg_url, data=json.dumps(data))
        result = json.loads(r.text)
        if result['errcode'] == 0:
            logger.info('企业微信消息发送成功')
        else:
            logger.info('企业微信消息发送失败' + str(result))


def pushplus(msg, token):
    pushplus_url = 'http://pushplus.hxtrip.com/send'
    data = {
        'token': token,
        'title': 'QQ消息',
        'content': msg,
        'template': 'html'
    }
    r = requests.post(url=pushplus_url, data=data)
    result = xmltodict.parse(r.text)
    if result['ResultT']['code'] == '200':
        logger.info('pushplus消息发送成功')
    else:
        logger.info('pushplus消息发送失败' + str(result))


def main(msg):
    pushplus_token = config.push_way['pushplus_token']
    qywx_config = config.push_way['qywx_config']
    if pushplus_token != '':
        pushplus(msg, pushplus_token)
    if qywx_config != '':
        qywx(msg, qywx_config)
