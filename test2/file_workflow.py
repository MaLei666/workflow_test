# #-*- coding:utf-8 -*-
# # @author : MaLei
# # @datetime : 2020/4/21 7:22 下午
# # @file : file_workflow.py
# # @software : PyCharm
#
# from SpiffWorkflow.specs import WorkflowSpec,ExclusiveChoice,Simple,Cancel
# from SpiffWorkflow.serializer.json import JSONSerializer
# from SpiffWorkflow.operators import Equal,Attrib
# from SpiffWorkflow import Workflow
# import json
# def file_open(msg):
#     print("file:",msg)
#
#
# class DoubleCheck(WorkflowSpec):
#     '''一、 子类不重写__init__ ， 实例化子类时，会自动调用父类定义的__init__
#
#        二、 子类重写了__init__时，实例化子类，就不会调用父类已经定义的__init__
#
#        三、为了能使用或扩展父类的行为，要显示调用父类的__init__方法，有以下两种调用方式：1，调用未绑定的父类构造方法。2，super继承'''
#     def __init__(self):
#         WorkflowSpec.__init__(self)  #调用未绑定的超类构造方法【必须显式调用父类的构造方法，否则不会执行父类构造方法】
#         people1_choice=ExclusiveChoice(self,'people1')  #定义排他性选择任务
#         self.start.connect(people1_choice)  #start方法调用StartTask模块，实现放置在工作流开始处的任务，没有输入，至少有一个输出，
#         cancel=Cancel(self,'workflow_aborted') # 定义取消工作流程
#         people1_choice.connect(cancel)
#         people2_choice=ExclusiveChoice(self,'people2')
#         cond=Equal(Attrib('confirmation'),'yes')   #equal运算符，Attrib标记一个值，使它可以通过valueof()被识别为一个属性值
#         people1_choice.connect_if(cond,people2_choice)  #如果条件匹配，则连接执行taskspec,
#         people2_choice.connect(cancel) #如果没有其他条件匹配，则连接执行的任务规范。
#         open=Simple(self,'file_open')
#         people2_choice.connect_if(cond,open)
#         open.completed_event.connect(file_open)
#
# # spec=DoubleCheck()
# #
# # serializer=JSONSerializer()
# # """
# #     执行工作流的引擎。
# #
# #     它本质上是一个管理所有分支的工具。
# #
# #     工作流也是存放正在运行的工作流的数据的地方。
# # """
# # workflow=Workflow(spec)
# # data=workflow.serialize(serializer)
# # pretty=json.dumps(json.loads(data),indent=4,separators=(',',':'))
# # open('workflow-spec.json','w').write(pretty)
#
# serializer = JSONSerializer()
# with open('workflow-spec.json') as fp:
#     workflow_json = fp.read()
# spec = WorkflowSpec.deserialize(serializer, workflow_json)
# open('workflow-spec.py','w').write(spec)


from __future__ import print_function
from SpiffWorkflow.specs import WorkflowSpec, ExclusiveChoice, Simple, Cancel
from SpiffWorkflow.operators import Equal, Attrib


def my_nuclear_strike(msg):
    print("Launched:", msg)


class DoubleDeckBox(WorkflowSpec):
    def __init__(self):
        WorkflowSpec.__init__(self)
        peopleA_choice = ExclusiveChoice(self, 'peopleA')
        self.start.connect(peopleA_choice)
        cancel = Cancel(self, 'workflow_aborted')
        peopleA_choice.connect(cancel)
        peopleB_choice = ExclusiveChoice(self, 'peopleB')
        cond = Equal(Attrib('confirmation'), 'yes')
        peopleA_choice.connect_if(cond, peopleB_choice)
        peopleB_choice.connect(cancel)
        strike = Simple(self, 'nuclear_strike')
        peopleB_choice.connect_if(cond, strike)
        strike.completed_event.connect(my_nuclear_strike)

