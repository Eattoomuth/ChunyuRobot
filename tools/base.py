# -*- coding: utf-8 -*-
import commands
import os
import subprocess
import traceback
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
import math
from image_tools import draw_rec, draw_arrow
from tools import utils
from time import sleep
from log_utils import log_by_run_time, get_run_id

__author__ = 'wgx'

PNG_DIR_ROOT = '../assets/pngs'
LOG_DIR_ROOT = '../assets/logs'
ADB_LOG_DIR_ROOT = '../assets/adb_logs'
APPIUM_LOG_DIR_ROOT = '../assets/appium_logs'


class EvaRobot(object):
    """
    Configure:
    platform_version :  Android system version
    device_type :       Android Emulator or Real Device
    apk_path :          The relative path of the apk
    package_name :      The apk's package name
    launch_activity:    The activity to start
    port :              One port one instance, for multi-phone test.
    """

    platform_version = '4.2'
    apk_path = '../assets/apks/ChunyuDoctorTest_7.5.0_manual.apk'
    package_name = 'me.chunyu.ChunyuDoctor'
    launch_activity = '.Activities.WelcomeActivity'

    def __init__(self, port, device_name, need_appium_server=True):
        """
        初始化，Appium默认支持多设备，所以如果存在多个设备需要建立多个Appium server，每个端口对应一个设备
        :param port:    Appium server 的端口
        :param device_name: 设备名称
        :param need_appium_server   是否需要一个启动一个appium的server
        注意：如果指定端口的server已存在，则会干掉原来的进程，意味着原server上的测试会挂掉
        """
        self.port = port
        self.device_name = device_name
        self.run_id = get_run_id()

        # 新建一个appium server，每次执行对应一个，port不能重复
        if need_appium_server:
            self.appium_log_path = os.path.join(APPIUM_LOG_DIR_ROOT, self.run_id + '.log')
            log_by_run_time('Create appium log path : ' + os.path.abspath(self.appium_log_path))
            self.start_appium()

        # 默认的配置，可以重写Eva来修改定制
        desired_caps = {'platformName': 'Android'}
        desired_caps['platformVersion'] = self.platform_version
        desired_caps['deviceName'] = self.device_name
        desired_caps['app'] = os.path.abspath(os.path.join(os.path.dirname(__file__), self.apk_path))
        desired_caps['appPackage'] = self.package_name
        desired_caps['appActivity'] = self.launch_activity

        log_by_run_time('Connect to device ... ')
        self.driver = webdriver.Remote('http://localhost:%d/wd/hub' % int(self.port), desired_caps)

        # log_by_run_time('context : ' + str(self.driver.contexts))
        # self.driver.switch_to.context('WEBVIEW_1')
        # log_by_run_time('context : ' + str(self.driver.contexts))

        # 如果发现已安装，先卸载旧的
        log_by_run_time('Reinstall ... ')
        if self.driver.is_app_installed(self.package_name):
            # Appium的uninstall在多设备时有bug
            # self.driver.remove_app(self.package_name)
            commands.getstatusoutput('adb -s %s uninstall %s' % (self.device_name, self.package_name))
        # install 也不好使，醉了
        # self.driver.install_app(os.path.abspath(self.apk_path))
        commands.getstatusoutput('adb -s %s install %s' % (self.device_name, self.apk_path))

        # 事件、事件计数
        self.action = TouchAction(self.driver)
        self.opt_count = 0

        # 建立图片log的目录，根据执行时间
        self.png_log_dir = os.path.join(PNG_DIR_ROOT, self.run_id)
        self.adb_log_dir = os.path.join(ADB_LOG_DIR_ROOT, self.run_id)
        log_by_run_time('Create png log path : ' + os.path.abspath(self.png_log_dir))
        log_by_run_time('Create adb log path : ' + os.path.abspath(self.adb_log_dir))
        if not os.path.exists(self.png_log_dir):
            os.system('mkdir -p ' + self.png_log_dir)
            os.system('mkdir -p ' + self.adb_log_dir)

        # 启动首页，因为卸载过，原来的首页已经被干掉了
        self.driver.start_activity(self.package_name, self.launch_activity)

        # 获取分辨率，可能不太准，是最外层layout的大小
        eles = self.driver.find_elements_by_xpath(utils.android_framelayout)
        self.max_x = eles[0].size['width']
        self.max_y = eles[0].size['height']
        log_by_run_time('Screen size(px) : (%d, %d)' % (self.max_x, self.max_y))

        # 待执行的过程，应该是一堆Process的实例
        self.process_list = []
        self.pass_count = 0

    def start_appium(self):
        """
        根据端口启动一个appium server
        """
        # 检查是否已有指定端口的服务在运行
        status, output = commands.getstatusoutput('ps aux | grep "lib/server/main.js"')
        output_lines = output.split('\n')
        pid = None
        line_tag = False
        for line in output_lines:
            if line.find('node') != -1 and line.find(str(self.port)) != -1:
                params = line.split(' ')
                for i in range(1, len(params)):
                    if params[i].strip():
                        pid = params[i]
                        line_tag = True
                        break
            if line_tag:
                break
        if pid:
            log_by_run_time('Kill original running appium with port ' + str(self.port))
            status, output = commands.getstatusoutput('kill -9 ' + pid)
            log_by_run_time('Kill result: ' + str(status) + ' ' + str(output))

        appium_log_file = open(self.appium_log_path, 'w+')
        subprocess.Popen('sh /Users/wgx/.wgxtools/appium_start.sh ' + str(self.port) + ' ' + str(self.device_name),
                         shell=True, stdout=appium_log_file, stderr=appium_log_file)

        # 等待服务启动
        sleep(8)

    def start(self):
        """
        Start.
        """
        for process in self.process_list:
            try:
                process.start()
                self.pass_count += 1
            except Exception as e:
                # 出现异常，输出log
                self.generate_adb_logs()
                log_by_run_time(e.message)
                log_by_run_time(traceback.format_exc())
        self.quit()

    def generate_adb_logs(self, lines=5000):
        """
        输出当前logcat的log到文件，格式为：adb_log_执行时间_事件编号
        :param lines: 保存的log行数
        """
        adb_log_file_name = 'adb_log_%d.log' % self.opt_count
        adb_log_path = os.path.join(os.path.abspath(self.adb_log_dir), adb_log_file_name)
        os.system('adb -s ' + self.device_name + ' logcat -v time -t ' + str(lines) + ' > ' + adb_log_path)

    def quit(self):
        """
        Close the session.
        """
        self.generate_adb_logs()
        log_by_run_time('End.\n\nRun %d cases, %d passed.' % (len(self.process_list), self.pass_count))
        self.driver.quit()


class FailException(Exception):
    def __init__(self):
        Exception.__init__(self)


class EvaProcess(object):
    def __init__(self, robot):
        """
        执行这个process的robot
        """
        self.robot = robot
        self.robot.process_list.append(self)
        self.driver = self.robot.driver
        self.action = TouchAction(self.driver)

    def start(self):
        """
        仅供robot使用，开始测试流程
        """
        self.before_run()
        self.run()
        self.after_run()

    def before_run(self):
        """
        开始执行流程前执行
        """

    def after_run(self):
        """
        结束流程后执行
        """
        # 执行完，截图留念
        self.log('Saving last pic...')
        png_log_path = self.get_next_png_path()
        self.driver.save_screenshot(png_log_path)

    def run(self):
        """
        过程写在这里
        """
        pass

    def find_element_by_text(self, p_text):
        """
        Deal with the text selector.
        """
        return self.driver.find_element_by_android_uiautomator('new UiSelector().text("' + p_text + '")')

    def find_elements_by_text(self, p_text):
        """
        Deal with the text selector.
        """
        return self.driver.find_elements_by_android_uiautomator('new UiSelector().text("' + p_text + '")')

    # appium 搞不定
    # def check_toast_is(self, toast):
    #     """
    #     检查toast内容是否正确
    #     """
    #     png_log_path = self.get_next_png_path()
    #     self.driver.save_screenshot(png_log_path)
    #     self.log('Check on toast : ' + toast)

    def tap_on_ele(self, ele):
        """
        Tap on a element
        """
        # 截图，画方块
        png_log_path = self.get_next_png_path()
        self.driver.save_screenshot(png_log_path)
        draw_rec(png_log_path, png_log_path,
                 (ele.location['x'] + ele.size['width'] / 2, ele.location['y'] + ele.size['height'] / 2))

        # 执行点击
        self.log('Tap on ele : ' + str(ele.location))
        self.action.tap(ele).perform()

    def tap_on_text(self, p_text):
        """
        Tap on text.
        """
        ele = self.find_element_by_text(p_text)
        # 截图，画方块
        png_log_path = self.get_next_png_path()
        self.driver.save_screenshot(png_log_path)
        draw_rec(png_log_path, png_log_path,
                 (ele.location['x'] + ele.size['width'] / 2, ele.location['y'] + ele.size['height'] / 2))

        # 执行点击
        self.log('Tap on text : ' + p_text)
        self.action.tap(ele).perform()

    def tap_on_id(self, id):
        """
        点击ID的ele
        """
        ele = self.find_element_by_id(id)
        # 截图，画方块
        png_log_path = self.get_next_png_path()
        self.driver.save_screenshot(png_log_path)
        draw_rec(png_log_path, png_log_path,
                 (ele.location['x'] + ele.size['width'] / 2, ele.location['y'] + ele.size['height'] / 2))

        self.log('Tap on id : ' + str(id))
        self.action.tap(ele).perform()

    def find_element_by_id(self, id):
        """
        根据ID找控件
        """
        return self.driver.find_element_by_id(id)

    def find_elements_by_id(self, id):
        """
        根据ID找控件
        """
        return self.driver.find_elements_by_id(id)


    def scroll_ele_to_ele(self, start_ele, end_ele, direction, wait=0):
        """
        从一个ele滚到另一个ele
        :param wait: ele to ele貌似不用长按
        """
        start_x = start_ele.location['x'] + start_ele.size['width'] / 2
        start_y = start_ele.location['y'] + start_ele.size['height'] / 2
        end_x = end_ele.location['x'] + end_ele.size['width'] / 2
        end_y = end_ele.location['y'] + end_ele.size['height'] / 2

        # 截图，画箭头
        png_log_path = self.get_next_png_path()
        self.driver.save_screenshot(png_log_path)
        draw_arrow(png_log_path, png_log_path, (start_x, start_y), direction)

        if direction == utils.DIRECTION_UP:
            direction_text = 'up'
            distance = math.fabs(end_y - start_y)
        elif direction == utils.DIRECTION_DOWN:
            direction_text = 'down'
            distance = math.fabs(end_y - start_y)
        elif direction == utils.DIRECTION_LEFT:
            direction_text = 'left'
            distance = math.fabs(end_x - start_x)
        else:
            direction_text = 'right'
            distance = math.fabs(end_x - start_x)

        # 滚起来
        self.log(
            'Scroll from : ' + str((start_x, start_y)) + ' direction : ' + direction_text + ' distance : '
            + str(distance))
        self.action.press(start_ele).wait(wait).move_to(end_ele).release().perform()

        # press 指定的位置，appium python client貌似有bug
        # def scroll_from_point(self, start, direction, distance=500, wait=2000):
        #     """
        #     Perform a scroll event.
        #     :param start:       Start location.
        #     :param direction:   Direction(The finger moving direction)
        #     :param distance:    Distance, default 500px
        #     :param wait:        Press delay time
        #     """
        #     # 截图，画箭头
        #     png_log_path = self.get_next_png_path()
        #     self.driver.save_screenshot(png_log_path)
        #     draw_arrow(png_log_path, png_log_path, start, direction)
        #
        #     # 计算滚动的停止坐标
        #     if direction == utils.DIRECTION_UP:
        #         end_x = start[0]
        #         end_y = start[1] - distance
        #         if end_y < 0:
        #             end_y = 0
        #         direction_text = 'up'
        #     elif direction == utils.DIRECTION_DOWN:
        #         end_x = start[0]
        #         end_y = start[1] + distance
        #         if end_y > self.robot.max_y:
        #             end_y = self.robot.max_y
        #         direction_text = 'down'
        #     elif direction == utils.DIRECTION_LEFT:
        #         end_x = start[0] - distance
        #         end_y = start[1]
        #         if end_x < 0:
        #             end_x = 0
        #         direction_text = 'left'
        #     else:
        #         end_x = start[0] + distance
        #         end_y = start[1]
        #         if end_x > self.robot.max_x:
        #             end_x = self.robot.max_x
        #         direction_text = 'right'
        #
        #     # 滚起来
        #     self.log(
        #         'Scroll from : ' + str(start) + ' direction : ' + direction_text + ' distance : ' + str(distance))
        #
        #     # base_ele = self.find_elements_by_widget(utils.android_framelayout)[0]
        #     self.action.press(el=None, x=500, y=500).wait(5000).perform()
        #     self.action.press(el=None, x=510, y=510).wait(5000).perform()
        #     self.action.press(el=None, x=520, y=520).wait(5000).perform()
        #     self.action.press(el=None, x=530, y=530).wait(5000).perform()
        #     self.action.press(el=None, x=540, y=540).wait(5000).perform()
        #     self.action.press(el=None, x=100, y=100).wait(5000).perform()
        # self.action.press(, x=500, y=500).wait(5000).move_to(base_ele, x=500,
        #                                                              y=1000).release().perform()

    def log(self, text):
        log_by_run_time(str(self.robot.opt_count) + ' : ' + str(text))

    def find_elements_by_widget(self, widget):
        """
        Find elements by widget.
        """
        return self.driver.find_elements_by_xpath(widget)

    def find_element_by_widget(self, widget):
        """
        Find element by widget.
        """
        return self.driver.find_element_by_xpath(widget)

    def get_next_png_path(self):
        """
        Generate the png path
        """
        png_path = os.path.join(self.robot.png_log_dir, 'png_log_' + str(self.robot.opt_count) + '.png')
        self.robot.opt_count += 1
        return png_path

    def start_activity(self, activity_path):
        """
        打开页面
        """
        self.log('Start activity : ' + activity_path)
        self.driver.start_activity(self.robot.package_name, activity_path)

    def input(self, ele, text):
        """
        输入
        """
        # 截图，画方块
        png_log_path = self.get_next_png_path()
        self.driver.save_screenshot(png_log_path)
        draw_rec(png_log_path, png_log_path,
                 (ele.location['x'] + ele.size['width'] / 2, ele.location['y'] + ele.size['height'] / 2))

        # 输入
        self.log('input : ' + text)
        ele.send_keys(text)

    def switch_to_flight_mode(self):
        """
        Value (Alias)      | Data | Wifi | Airplane Mode
            -------------------------------------------------
            0 (None)           | 0    | 0    | 0
            1 (Airplane Mode)  | 0    | 0    | 1
            2 (Wifi only)      | 0    | 1    | 0
            4 (Data only)      | 1    | 0    | 0
            6 (All network on) | 1    | 1    | 0
        """
        self.driver.set_network_connection(1)

    def switch_to_network_open(self):
        self.driver.set_network_connection(6)

    def switch_to_network_close(self):
        self.driver.set_network_connection(0)

    def press_back(self):
        """
        返回
        """
        # 截图
        png_log_path = self.get_next_png_path()
        self.driver.save_screenshot(png_log_path)

        self.log('Back button pressed.')
        self.driver.keyevent(4)

    @staticmethod
    def delay(seconds):
        """
        延时
        """
        log_by_run_time('delay : ' + str(seconds))
        sleep(seconds)
