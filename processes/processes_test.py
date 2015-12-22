# -*- coding: utf-8 -*-
from tools.base import EvaProcess, EvaRobot
from processes.main_common import start_processes

__author__ = 'wgx'


# 这个文件的case都是写着玩的


class ProcessTest(EvaProcess):
    def __init__(self, robot):
        EvaProcess.__init__(self, robot)

    def run(self):
        self.delay(2)
        self.press_back()
        self.delay(3)


class TestRobot(EvaRobot):
    apk_path = '../assets/apks/app-debug.apk'
    package_name = 'me.chunyu.testapk'
    launch_activity = '.MainActivity'


if __name__ == '__main__':
    start_processes(TestRobot, [ProcessTest, ], False)