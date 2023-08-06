======================
pywe-subscribe-message
======================

Wechat Subscribe Message Module for Python.

Sandbox
=======

* https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login

Installation
============

::

    pip install pywe-subscribe-message


Usage
=====

::

    from pywe_subscribe_message.subscribemsg import SubscribeMessage, send_subscribe_template_message, send_wxa_subscribe_template_message


Method
======

::

    class SubscribeMessage(BaseToken):
        def __init__(self, appid=None, secret=None, token=None, storage=None):
            super(SubscribeMessage, self).__init__(appid=appid, secret=secret, token=token, storage=storage)

    def send_subscribe_template_message(self, user_id, template_id, data, url=None, scene=None, title=None, miniprogram=None, mini_program=None, miniappid=None, minipagepath=None, appid=None, secret=None, token=None, storage=None):

    def send_wxa_subscribe_template_message(self, user_id, template_id, data, page=None, miniprogram_state=None, lang=None, appid=None, secret=None, token=None, storage=None):

