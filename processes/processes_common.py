# -*- coding: utf-8 -*-
from tools import utils
from tools.base import EvaProcess, EvaRobot

__author__ = 'wgx'


class ProcessDealWithGuide(EvaProcess):
    """
    处理引导页，一般只有第一次启动会出现
    """
    def __init__(self, robot):
        EvaProcess.__init__(self, robot)

    def run(self):
        try:
            self.tap_on_id('float_layer')
        except:
            self.log("Guide page didn't appear")


class ProcessDealWithUpdateDialog(EvaProcess):
    """
    每次进入首页都要执行这个，因为不知道什么时候会蹦出来
    """
    def __init__(self, robot):
        EvaProcess.__init__(self, robot)

    def run(self):
        # 欢迎页等待
        self.delay(3)

        # 处理update dialog
        try:
            self.tap_on_text('以后再说')
        except:
            self.log("Update dialog didn't appear")


# class TestRobot(EvaRobot):
#     apk_path = '../assets/apks/app-debug.apk'
#     package_name = 'me.chunyu.testapk'
#     launch_activity = '.MainActivity'


# if __name__ == '__main__':
#     robot = TestRobot()
#     # process_start = ProcessStartUp(robot)
#     process = ProcessTest(robot)
#     robot.start()


