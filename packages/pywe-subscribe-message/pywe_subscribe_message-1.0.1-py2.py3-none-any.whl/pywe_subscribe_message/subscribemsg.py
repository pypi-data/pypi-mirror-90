# -*- coding: utf-8 -*-

from pywe_token import BaseToken, final_access_token


class SubscribeMessage(BaseToken):
    def __init__(self, appid=None, secret=None, token=None, storage=None):
        super(SubscribeMessage, self).__init__(appid=appid, secret=secret, token=token, storage=storage)
        # 公众号订阅消息, Refer: https://developers.weixin.qq.com/doc/offiaccount/Message_Management/One-time_subscription_info.html
        # 第二步：通过API推送订阅模板消息给到授权微信用户
        self.WECHAT_SEND_SUBSCRIBE_TEMPLATE_MESSAGE = self.API_DOMAIN + '/cgi-bin/message/template/subscribe'
        # 小程序订阅消息, Refer: https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/subscribe-message/subscribeMessage.send.html
        # subscribeMessage.send
        self.WECHAT_SEND_WXA_SUBSCRIBE_TEMPLATE_MESSAGE = self.API_DOMAIN + '/cgi-bin/message/subscribe/send'

    def send_subscribe_template_message(self, user_id, template_id, data, url=None, scene=None, title=None, miniprogram=None, mini_program=None, miniappid=None, minipagepath=None, appid=None, secret=None, token=None, storage=None):
        if not miniprogram and not mini_program and miniappid and minipagepath:
            miniprogram = {
                'appid': miniappid,
                'pagepath': minipagepath,
            }
        return self.post(
            self.WECHAT_SEND_SUBSCRIBE_TEMPLATE_MESSAGE,
            params={
                'access_token': final_access_token(self, appid=appid, secret=secret, token=token, storage=storage),
            },
            data={
                'touser': user_id,
                'template_id': template_id,
                'url': url,
                'miniprogram': miniprogram or mini_program,
                'scene': scene,
                'title': title,
                'data': data,
            },
        )

    def send_wxa_subscribe_template_message(self, user_id, template_id, data, page=None, miniprogram_state=None, lang=None, appid=None, secret=None, token=None, storage=None):
        return self.post(
            self.WECHAT_SEND_WXA_SUBSCRIBE_TEMPLATE_MESSAGE,
            params={
                'access_token': final_access_token(self, appid=appid, secret=secret, token=token, storage=storage),
            },
            data={
                'touser': user_id,
                'template_id': template_id,
                'page': page,
                'miniprogram_state': miniprogram_state,
                'lang': lang,
                'data': data,
            },
        )


subscribemessage = SubscribeMessage()
send_subscribe_template_message = subscribemessage.send_subscribe_template_message
send_wxa_subscribe_template_message = subscribemessage.send_wxa_subscribe_template_message
