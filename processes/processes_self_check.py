# -*- coding: utf-8 -*-
from processes.main_common import start_processes
from processes.processes_common import ProcessDealWithUpdateDialog, ProcessDealWithGuide
from tools import utils
from tools.base import EvaProcess, EvaRobot, FailException

__author__ = 'wgx'

# 自查的用例写这里

# 搜索的关键字
SEARCH_KEY_EMPTY = '234'
SEARCH_KEY_DRUG = 'jiaxiaozuo '
SEARCH_KEY_DISEASE0 = 'tangniaobing '
SEARCH_KEY_DISEASE1 = 'ganmao '
SEARCH_KEY_SYMPTOM = 'kesou '



# 搜索
class ProcessSelfSearch1(EvaProcess):
    """
    对应自查用例1
    """

    def __init__(self, robot):
        EvaProcess.__init__(self, robot)

    def run(self):
        self.start_activity('.Activities.MainActivity600')
        self.tap_on_text('自我诊断')
        self.tap_on_text('搜索症状、疾病、药品')
        eles = self.find_elements_by_widget(utils.android_edittext)
        if len(eles) > 0:
            self.input(eles[0], SEARCH_KEY_EMPTY)
        self.tap_on_id('search_bar_button')
        self.delay(1)
        eles = self.find_elements_by_text('没有搜索到相应的内容')
        if len(eles) > 0:
            return
        else:
            raise FailException


class ProcessSelfSearch3(EvaProcess):
    """
    在用例1之后执行，对应用例3
    "1.自我诊断tab点击搜索框；
    2.点击搜索历史列表项"
    """

    def __init__(self, robot):
        EvaProcess.__init__(self, robot)

    def run(self):
        self.press_back()
        eles = self.find_elements_by_text(SEARCH_KEY_EMPTY)
        if len(eles) > 0:
            return
        else:
            raise FailException


class ProcessSelfSearch4(EvaProcess):
    """
    必须在3之后执行，对应用例4、5
    "1.自我诊断tab点击搜索框；
    2.点击‘清空搜索历史’按钮
    3.确定"
    """

    def __init__(self, robot):
        EvaProcess.__init__(self, robot)

    def run(self):
        self.tap_on_text('清空搜索历史')
        self.tap_on_text('确定')
        if self.find_elements_by_text('清空搜索历史'):
            raise FailException
        else:
            return


class ProcessSelfSearch6(EvaProcess):
    """
    对应6，要预先调好中文输入法，必须智能一点的，否则会悲剧
    附近药店，发现bug一枚，一会改掉
    "1.自我诊断tab点击搜索框；
    2.输入“甲硝唑”，点击搜索按钮
    3.点击“查看更多药品详情”
    3.点击页面下方“附近药店”按钮；"
    """

    def __init__(self, robot):
        EvaProcess.__init__(self, robot)

    def run(self):
        self.start_activity('.Activities.MainActivity600')
        self.tap_on_text('自我诊断')
        self.tap_on_text('搜索症状、疾病、药品')

        eles = self.find_elements_by_widget(utils.android_edittext)
        if len(eles) > 0:
            self.input(eles[0], SEARCH_KEY_DRUG)
        else:
            raise FailException
        self.tap_on_id('search_bar_button')
        self.delay(1)
        self.tap_on_text('查看更多药品详情')
        self.tap_on_text('附近药店')


class ProcessSelfSearch7(EvaProcess):
    """
    对应7，要预先调好中文输入法，必须智能一点的，否则会悲剧
    附近药店，发现bug一枚，一会改掉
    "1.自我诊断tab点击搜索框；
    2.输入“糖尿病”，点击搜索按钮
    3.点击‘查看更多疾病信息’链接"
    """

    def __init__(self, robot):
        EvaProcess.__init__(self, robot)

    def run(self):
        self.start_activity('.Activities.MainActivity600')
        self.tap_on_text('自我诊断')
        self.tap_on_text('搜索症状、疾病、药品')

        eles = self.find_elements_by_widget(utils.android_edittext)
        if len(eles) > 0:
            self.input(eles[0], SEARCH_KEY_DISEASE0)
        else:
            raise FailException
        self.tap_on_id('search_bar_button')
        self.delay(1)
        self.tap_on_text('查看更多疾病信息')
        if not self.find_elements_by_text('症状'):
            raise FailException


class ProcessSelfSearch8(EvaProcess):
    """
    8
    "1.自我诊断tab点击搜索框；
    2.输入“咳嗽”，点击搜索按钮"
    """
    def __init__(self, robot):
        EvaProcess.__init__(self, robot)

    def run(self):
        self.start_activity('.Activities.MainActivity600')
        self.tap_on_text('自我诊断')
        self.tap_on_text('搜索症状、疾病、药品')

        eles = self.find_elements_by_widget(utils.android_edittext)
        if len(eles) > 0:
            self.input(eles[0], SEARCH_KEY_SYMPTOM)
        else:
            raise FailException

        if not self.find_elements_by_text('感冒'):
            raise FailException


class ProcessSelfSearch10(EvaProcess):
    """
    10
    "1.自我诊断tab点击搜索框；
    2.输入“感冒”，点击搜索按钮
    3.可能的治疗方法中点击检查项（如，血常规）"
    """
    def __init__(self, robot):
        EvaProcess.__init__(self, robot)

    def run(self):
        self.start_activity('.Activities.MainActivity600')
        self.tap_on_text('自我诊断')
        self.tap_on_text('搜索症状、疾病、药品')

        eles = self.find_elements_by_widget(utils.android_edittext)
        if len(eles) > 0:
            self.input(eles[0], SEARCH_KEY_DISEASE1)
        else:
            raise FailException

        self.tap_on_text('血常规（检查）')
        if not self.find_elements_by_text('介绍'):
            raise FailException


class ProcessSelfSearch10(EvaProcess):
    """
    10
    "1.自我诊断tab点击搜索框；
    2.输入“感冒”，点击搜索按钮
    3.可能的治疗方法中点击检查项（如，血常规）"
    """
    def __init__(self, robot):
        EvaProcess.__init__(self, robot)

    def run(self):
        self.start_activity('.Activities.MainActivity600')
        self.tap_on_text('自我诊断')
        self.tap_on_text('搜索症状、疾病、药品')

        eles = self.find_elements_by_widget(utils.android_edittext)
        if len(eles) > 0:
            self.input(eles[0], SEARCH_KEY_DISEASE1)
        else:
            raise FailException

        self.tap_on_text('血常规（检查）')
        if not self.find_elements_by_text('介绍'):
            raise FailException



if __name__ == '__main__':
    start_processes(EvaRobot, [
        ProcessDealWithUpdateDialog,
        ProcessDealWithGuide,
        ProcessSelfSearch8,
        ProcessSelfSearch10,
    ], False)
