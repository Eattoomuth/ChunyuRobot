# -*- coding: utf-8 -*-

from tools import utils
from tools.base import EvaProcess

__author__ = 'wgx'


# 登录的用例写这里

class ProcessPhoneLogin0(EvaProcess):
    """
    正常的手机登录
    """
    user_name = '12312345678'
    user_pass = '111111'

    def __init__(self, robot):
        EvaProcess.__init__(self, robot)

    def run(self):
        self.tap_on_text('个人中心')
        self.tap_on_text('登录/注册')
        self.tap_on_text('登录')
        t_login_inputs = self.find_elements_by_widget(utils.android_edittext)
        if len(t_login_inputs) >= 2:
            self.input(t_login_inputs[0], self.user_name)
            self.input(t_login_inputs[1], self.user_pass)
        t_login_btn2 = self.find_elements_by_text('登录')[1]
        self.tap_on_ele(t_login_btn2)

        self.delay(2)


class ProcessLogout(EvaProcess):
    """
    注销登录
    """
    def __init__(self, robot):
        EvaProcess.__init__(self, robot)

    def run(self):
        # self.start_activity('.Activities.MainActivity600')
        self.tap_on_text('个人中心')
        self.tap_on_text('设置与帮助')

        self.scroll_ele_to_ele(self.find_element_by_text('春雨客服'), self.find_element_by_text('消息通知'),
                               utils.DIRECTION_DOWN)
        self.tap_on_text('注销')
        self.delay(1)

# Webview 暂时搞不定
# class ProcessPhoneLogin1(EvaProcess):
#     """
#     新浪微博首次登录，从首页开始，到手机号绑定结束
#     """
#     sina_user_name = 'chunyu_test@126.com'
#     sina_user_pass = 'chunyutest'
#
#     def __init__(self, robot):
#         EvaProcess.__init__(self, robot)
#
#     def run(self):
#         self.tap_on_text('个人中心')
#         self.tap_on_text('登录/注册')
#         self.tap_on_id('login_button_sina_login')
#         eles = self.find_elements_by_widget(utils.android_edittext)
#         if len(eles) >= 2:
#             self.input(eles[0], self.sina_user_name)
#             self.input(eles[1], self.sina_user_pass)
#         # self.tap_on_text('登录')
#
#         # self.delay(2)


# if __name__ == '__main__':
#     robot = EvaRobot()
#     ProcessStartUp(robot)
#     ProcessPhoneLogin0(robot)
#     ProcessLogout(robot)
#     # ProcessPhoneLogin1(robot)
#     robot.start()
