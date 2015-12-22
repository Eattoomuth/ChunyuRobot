# -*- coding: utf-8 -*-
import os
import time
from tools.base import EvaRobot
from processes import processes_login

__author__ = 'wgx'

import commands
import threading

# 端口从4700开始
port_count = 4700
running_devices = []

mutex = threading.Lock()


def get_next_robot(robot_name, need_appium_server=True):
    global port_count
    os.system('adb devices')
    status, output = commands.getstatusoutput('adb devices')
    output_lines = output.split('\n')
    device_name = None
    if status == 0 and len(output_lines) > 2:
        output_count = len(output_lines)
        for i in range(1, output_count - 1):
            tmp_device_name = output_lines[i].split('\t')[0]
            if tmp_device_name not in running_devices:
                device_name = tmp_device_name
                running_devices.append(device_name)
                break

    if device_name:
        if mutex.acquire(1):
            robot = robot_name(port_count, device_name, need_appium_server)
            port_count += 1
            mutex.release()
            return robot

    print 'No device available.'
    return None


def put_in(robot_name, process_list, need_appium_server=True):
    robot = get_next_robot(robot_name, need_appium_server)
    if robot:
        for chunyu_process in process_list:
            chunyu_process(robot)
        robot.start()


def start_processes(robot_name, process_list, need_appium_server=True):
    """
    启动一个新的测试，一个测试对应一个设备和一个appium server端口
    """
    threading.Thread(target=put_in, args=(robot_name, process_list, need_appium_server)).start()


if __name__ == '__main__':
    start_processes(EvaRobot, [processes_login.ProcessDealWithUpdateDialog, processes_login.ProcessPhoneLogin0])
    # start_processes(EvaRobot, [process_login.ProcessStartUp, process_login.ProcessPhoneLogin0])
    # put_in(EvaRobot, [process_login.ProcessStartUp, process_login.ProcessPhoneLogin0])


