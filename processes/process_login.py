# -*- coding: utf-8 -*-

from tools import utils
from tools.base import EvaProcess, EvaRobot

__author__ = 'wgx'


class ProcessStartUp(EvaProcess):
    def __init__(self, robot):
        EvaProcess.__init__(self, robot)

    def run(self):
        """
        第一次启动首页或者长时间未启动首页的时候必须要执行这个过程
        """
        # 欢迎页等待
        self.delay(5)

        # 处理update dialog
        try:
            self.tap_on_text('以后再说')
        except:
            self.log("Update dialog didn't appear")

        # 处理引导
        guide_ele = self.find_elements_by_widget(utils.android_imageview)[0]
        self.tap_on_ele(guide_ele)


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


class ProcessPhoneLogin1(EvaProcess):
    """
    检查未输入密码的情况
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
        t_login_btn2 = self.find_elements_by_text('登录')[1]
        self.tap_on_ele(t_login_btn2)
        self.check_toast_is('请输入密码')
        # self.delay(2)


if __name__ == '__main__':
    robot = EvaRobot()
    ProcessStartUp(robot)
    ProcessPhoneLogin0(robot)
    ProcessLogout(robot)
    ProcessPhoneLogin1(robot)
    robot.start()
