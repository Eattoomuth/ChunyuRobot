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
        self.delay(3)

        # 处理update dialog
        try:
            self.tap_on_text('以后再说')
        except:
            self.log("Update dialog didn't appear")

        # 处理引导
        guide_ele = self.find_elements_by_widget(utils.android_imageview)[0]
        self.tap_on_ele(guide_ele)


class ProcessLogin(EvaProcess):
    user_name = '12312345678'
    user_pass = '111111'

    def __init__(self, robot):
        EvaProcess.__init__(self, robot)

    def run(self):
        """
        常规的登录，没有任何验证
        """
        self.tap_on_text('个人中心')
        self.tap_on_text('登录/注册')
        self.tap_on_text('登录')
        t_login_inputs = self.find_elements_by_widget(utils.android_edittext)
        if len(t_login_inputs) >= 2:
            self.input(t_login_inputs[0], self.user_name)
            self.input(t_login_inputs[1], self.user_pass)
        t_login_btn2 = self.find_elements_by_text('登录')[1]
        self.tap_on_ele(t_login_btn2)

        self.delay(5)


class ProcessTest(EvaProcess):
    def __init__(self, robot):
        EvaProcess.__init__(self, robot)

    def run(self):
        # ele_start = self.find_element_by_text('私人医生')
        # ele_end = self.find_element_by_text('找医生')
        # self.scroll_ele_to_ele(ele_start, ele_end, utils.DIRECTION_UP)
        self.scroll_from_point((500, 500), utils.DIRECTION_DOWN)
        self.delay(5)


class TestRobot(EvaRobot):
    apk_path = '../assets/apks/app-debug.apk'
    package_name = 'me.chunyu.testapk'
    launch_activity = '.MainActivity'

if __name__ == '__main__':
    robot = TestRobot()
    # process_start = ProcessStartUp(robot)
    process = ProcessTest(robot)
    robot.start()


